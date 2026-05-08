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

    async def run_tester_agent(self, task_description: str, model: str = "qwen2.5:latest") -> str:
        """A sub-agent focused solely on testing code and finding bugs."""
        sys_prompt = "You are an expert software QA and Tester. Your job is to test code, find bugs, and report back. You cannot modify code, only run tests and return the results to the orchestrator."
        sys_prompt += f"\n\nAvailable Tools:\n{tool_manager.get_available_tools_description()}"

        prompt = f"Task: {task_description}\n\nThink step by step, use tools if needed (e.g. run_bash to execute pytest), and provide a final detailed test report."

        # For simplicity in this demo, the sub-agent runs a single zero-shot generation loop.
        # In a fully fleshed out system, this would be a while loop similar to the orchestrator.
        response = await ollama_service.generate_response(model, prompt, system=sys_prompt)

        # Check if the sub agent tried to use a tool
        import re
        match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
        if match:
            try:
                tool_call = json.loads(match.group(1))
                if "tool" in tool_call and "args" in tool_call:
                    tool_result = tool_manager.execute_tool(tool_call["tool"], **tool_call["args"])
                    # Send result back to model for final evaluation
                    eval_prompt = f"You used a tool. Result:\n{tool_result}\n\nBased on this result, write the final test report."
                    final_response = await ollama_service.generate_response(model, eval_prompt, system=sys_prompt)
                    return f"Tester Agent Report:\n{final_response}"
            except json.JSONDecodeError:
                pass

        return f"Tester Agent Report:\n{response}"

    async def run_researcher_agent(self, task_description: str, model: str = "qwen2.5:latest") -> str:
        """A sub-agent focused on searching the OS or internet for information."""
        sys_prompt = "You are an expert Researcher Agent. Your job is to find information, read files, or run bash commands to gather data, and return a summary."
        sys_prompt += f"\n\nAvailable Tools:\n{tool_manager.get_available_tools_description()}"

        prompt = f"Task: {task_description}\n\nUse tools to gather info, then summarize."
        response = await ollama_service.generate_response(model, prompt, system=sys_prompt)

        # Simple one-shot tool execution for the researcher
        import re
        match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
        if match:
            try:
                tool_call = json.loads(match.group(1))
                if "tool" in tool_call and "args" in tool_call:
                    tool_result = tool_manager.execute_tool(tool_call["tool"], **tool_call["args"])
                    eval_prompt = f"Tool Result:\n{tool_result}\n\nWrite final research summary."
                    final_response = await ollama_service.generate_response(model, eval_prompt, system=sys_prompt)
                    return f"Researcher Report:\n{final_response}"
            except json.JSONDecodeError:
                pass

        return f"Researcher Report:\n{response}"

sub_agent_manager = SubAgentManager()
