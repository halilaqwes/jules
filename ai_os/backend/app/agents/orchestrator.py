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
        self.system_prompt = """You are the Main Orchestrator Agent of an advanced AI OS.
Your job is to run 24/7 and achieve the user's goals.
You have access to tools. To use a tool, output a JSON block like this:
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

Always explain your reasoning before taking an action.
"""

    def set_model(self, model_name: str):
        self.model = model_name

    def set_goal(self, goal: str):
        self.current_goal = goal
        memory_service.set_memory("current_goal", goal)

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

        prompt = f"""
Current Goal: {self.current_goal}

Recent History:
{history}

What is your next step? (Use a tool if needed, otherwise just reason).
"""
        sys_prompt = self.system_prompt.replace("{tools}", tool_manager.get_available_tools_description())

        # Generate response
        response = await ollama_service.generate_response(self.model, prompt, system=sys_prompt)
        memory_service.log_event("orchestrator", "thought", response)

        # Check for tool call
        tool_call = self._parse_tool_call(response)
        if tool_call and "tool" in tool_call and "args" in tool_call:
            tool_name = tool_call["tool"]
            args = tool_call["args"]
            memory_service.log_event("orchestrator", "tool_call", f"Calling {tool_name} with {args}")

            # Execute tool
            tool_result = tool_manager.execute_tool(tool_name, **args)
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
