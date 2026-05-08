import asyncio
import json
import re
from typing import Optional, List, Dict
from app.services.ollama_service import ollama_service
from app.services.memory_service import memory_service
from app.tools.tool_manager import tool_manager

class Orchestrator:
    def __init__(self):
        self.is_running = False
        self.current_goal = ""
        self.model = "qwen2.5:latest" # Default, can be changed dynamically
        self.chat_history = []  # Store direct user-agent conversation
        self.system_prompt = """You are the Main Orchestrator Agent of an advanced AI OS with FULL system access.
Your job is to run autonomously 24/7. YOU MUST NEVER ASK THE USER FOR CONFIRMATION OR HELP.
If you encounter an error (e.g., from a tool or bash command), you must analyze the error and try a different approach immediately.
You are self-healing and self-correcting.

You have access to tools. To use a tool, output a JSON block exactly like this:
```json
{
  "tool": "tool_name",
  "args": {
    "arg_name": "arg_value"
  }
}
```

Available Tools:
{tools}

{lessons}

Always explain your reasoning before taking an action. If your previous action resulted in an error, explain why it failed and what your new strategy is.
"""

    def set_model(self, model_name: str):
        self.model = model_name

    def set_goal(self, goal: str):
        self.current_goal = goal
        memory_service.set_memory("current_goal", goal)

    async def handle_chat_message(self, message: str) -> str:
        """Handle a direct chat message from the user and respond."""
        self.chat_history.append({"role": "user", "content": message})

        # Build prompt specifically for chat
        sys_prompt = self.system_prompt.replace("{tools}", tool_manager.get_available_tools_description())
        lessons = memory_service.get_memory("learned_lessons") or []
        lessons_text = "Important Lessons:\n" + "\n".join([f"- {l}" for l in lessons]) if lessons else ""
        sys_prompt = sys_prompt.replace("{lessons}", lessons_text)

        # Inject relevant skills based on user message
        from app.skills.skill_manager import skill_manager
        skills_text = skill_manager.search_skills(message)
        if skills_text:
            sys_prompt += f"\n\n{skills_text}"

        chat_context = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.chat_history[-5:]])

        prompt = f"""
You are talking directly to the user.
Recent Conversation:
{chat_context}

Please respond to the User. You can use tools if needed to fulfill their request, or just talk to them normally.
"""
        response = await ollama_service.generate_response(self.model, prompt, system=sys_prompt)
        self.chat_history.append({"role": "agent", "content": response})

        # Check if a tool was requested during chat
        tool_call = self._parse_tool_call(response)
        if tool_call and "tool" in tool_call and "args" in tool_call:
             # We let the main loop handle the tool execution logic, or handle it here if it's immediate
             # For chat, executing immediately is better for UX
             tool_name = tool_call["tool"]
             args = tool_call["args"]
             if tool_name == "delegate_task":
                 from app.agents.sub_agents import sub_agent_manager
                 agent_type = args.get("agent_type")
                 task = args.get("task_description")
                 if agent_type in sub_agent_manager.sub_agents:
                     tool_result = await sub_agent_manager.sub_agents[agent_type](task, self.model)
                 else:
                     tool_result = f"Error: Sub-agent type '{agent_type}' not found."
             else:
                 tool_result = await tool_manager.execute_tool(tool_name, **args)

             # Feed tool result back to chat
             followup_prompt = f"Tool Result for {tool_name}:\n{tool_result}\n\nTell the user the result."
             response = await ollama_service.generate_response(self.model, followup_prompt, system=sys_prompt)
             self.chat_history.append({"role": "agent", "content": response})

        return response

    def _parse_tool_call(self, text: str) -> Optional[Dict]:
        """Extract tool call JSON from text."""
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return None

    async def _step(self):
        """Perform one execution step."""
        if not self.current_goal:
            await asyncio.sleep(1)
            return

        # Prepare context (recent events, goal)
        recent_events = memory_service.get_recent_events("orchestrator", limit=10)
        history = "\n".join([f"[{e['timestamp']}] {e['event_type']}: {e['content']}" for e in recent_events])

        # Fetch learned lessons to include in the system prompt
        lessons = memory_service.get_memory("learned_lessons") or []
        lessons_text = "Important Lessons Learned from Past Mistakes:\n" + "\n".join([f"- {l}" for l in lessons]) if lessons else ""

        prompt = f"""
Current Goal: {self.current_goal}

Recent History (including your tool results and errors):
{history}

What is your next step? Remember: Do NOT ask the user for help. If there is an error in history, fix it yourself.
"""
        sys_prompt = self.system_prompt.replace("{tools}", tool_manager.get_available_tools_description())
        sys_prompt = sys_prompt.replace("{lessons}", lessons_text)

        # Inject relevant skills based on current goal
        from app.skills.skill_manager import skill_manager
        skills_text = skill_manager.search_skills(self.current_goal)
        if skills_text:
            sys_prompt += f"\n\n{skills_text}"

        # Generate response
        response = await ollama_service.generate_response(self.model, prompt, system=sys_prompt)
        memory_service.log_event("orchestrator", "thought", response)

        # Check for tool call
        tool_call = self._parse_tool_call(response)
        if tool_call and "tool" in tool_call and "args" in tool_call:
            tool_name = tool_call["tool"]
            args = tool_call["args"]
            memory_service.log_event("orchestrator", "tool_call", f"Calling {tool_name} with {args}")

            # Special case for sub-agents (async tool execution)
            if tool_name == "delegate_task":
                from app.agents.sub_agents import sub_agent_manager
                agent_type = args.get("agent_type")
                task = args.get("task_description")
                if agent_type in sub_agent_manager.sub_agents:
                    tool_result = await sub_agent_manager.sub_agents[agent_type](task, self.model)
                else:
                    tool_result = f"Error: Sub-agent type '{agent_type}' not found."
            else:
                # Execute normal synchronous/async tool
                tool_result = await tool_manager.execute_tool(tool_name, **args)

            memory_service.log_event("orchestrator", "tool_result", str(tool_result))

        await asyncio.sleep(1)

    async def run_loop(self):
        """The 24/7 continuous execution loop."""
        self.is_running = True
        print("Orchestrator Agent started 24/7 loop.")
        while self.is_running:
            try:
                await self._step()
            except Exception as e:
                print(f"Error in orchestrator loop: {e}")
                memory_service.log_event("orchestrator", "error", str(e))
                await asyncio.sleep(5)

    def stop(self):
        self.is_running = False

orchestrator = Orchestrator()
