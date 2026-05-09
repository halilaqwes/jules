import json
from typing import Optional
from app.services.ollama_service import ollama_service
from app.services.memory_service import memory_service
from app.tools.tool_manager import tool_manager

class SubAgentManager:
    """Manages specific sub-agents that the Orchestrator can call upon."""

    def __init__(self):
        self.sub_agents = {
            "tester": self.run_tester_agent,
            "researcher": self.run_researcher_agent
        }

    async def _autonomous_loop(self, role_name: str, sys_prompt: str, task_description: str, model: str) -> str:
        """A generic autonomous loop for sub-agents."""
        import re
        history = []
        max_retries = 5
        retries = 0

        prompt = f"Task: {task_description}\n\nThink step by step. Use tools to achieve your goal. If a tool fails, DO NOT give up. Formulate a new plan and try a different tool or command."

        while retries < max_retries:
            response = await ollama_service.generate_response(model, prompt, system=sys_prompt)
            history.append(f"[{role_name} Thought]: {response}")

            match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if not match:
                # No tool used, must be the final report
                return f"{role_name} Final Report:\n{response}"

            try:
                tool_call = json.loads(match.group(1))
                if "tool" in tool_call and "args" in tool_call:
                    tool_name = tool_call["tool"]
                    tool_result = await tool_manager.execute_tool(tool_name, **tool_call["args"])

                    history.append(f"[Tool '{tool_name}' Result]: {tool_result}")

                    prompt = f"Previous actions:\n" + "\n".join(history[-3:]) + f"\n\nTool '{tool_name}' executed. Result:\n{tool_result}\n\nIf you have encountered an error, YOU MUST NOT give up. Fix the issue yourself using other tools. If the original task is complete, provide your final report without calling another tool."
                else:
                    break
            except json.JSONDecodeError:
                prompt = "Error: Invalid JSON format for tool call. Please output exactly valid JSON."

            retries += 1

        return f"{role_name} Report (Max Retries Reached):\n{response}"

    async def run_tester_agent(self, task_description: str, model: str = "qwen2.5:latest") -> str:
        """A sub-agent focused solely on testing code and finding bugs."""
        sys_prompt = "You are an expert software QA and Tester. Your job is to test code, find bugs, and report back. You cannot modify code, only run tests and return the results to the orchestrator. YOU NEVER GIVE UP. If a test fails to run, fix your test setup and run it again. ESCALATION PROTOCOL: If you fail after 2 attempts, use `ask_deepseek_oracle`."
        sys_prompt += f"\n\nAvailable Tools:\n{tool_manager.get_available_tools_description()}"
        return await self._autonomous_loop("Tester Agent", sys_prompt, task_description, model)

    async def run_researcher_agent(self, task_description: str, model: str = "qwen2.5:latest") -> str:
        """A sub-agent focused on searching the OS or internet for information."""
        sys_prompt = "You are an expert Researcher Agent. Your job is to find information, read files, or run bash commands to gather data, and return a summary. YOU NEVER GIVE UP. If a path is wrong, use `ls` to find the right path. If a web search fails, try a different query. ESCALATION PROTOCOL: If you fail after 2 attempts, use `ask_deepseek_oracle`."
        sys_prompt += f"\n\nAvailable Tools:\n{tool_manager.get_available_tools_description()}"
        return await self._autonomous_loop("Researcher Agent", sys_prompt, task_description, model)

sub_agent_manager = SubAgentManager()
