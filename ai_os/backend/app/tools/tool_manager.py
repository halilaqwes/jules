import json
import inspect
from typing import Callable, Dict, Any, List
from .os_tools import os_tools

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        self.register("read_file", os_tools.read_file, "Read the contents of a file. Args: filepath (str)")
        self.register("write_file", os_tools.write_file, "Write contents to a file. Args: filepath (str), content (str)")
        self.register("run_bash", os_tools.run_bash, "Run a bash command. Args: command (str)")

    def register(self, name: str, func: Callable, description: str):
        """Register a new tool dynamically."""
        self.tools[name] = {
            "function": func,
            "description": description
        }

    def get_available_tools_description(self) -> str:
        """Returns a string describing all available tools."""
        descriptions = []
        for name, tool_info in self.tools.items():
            descriptions.append(f"- {name}: {tool_info['description']}")
        return "\n".join(descriptions)

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name with the given arguments."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."

        func = self.tools[tool_name]["function"]
        try:
            return func(**kwargs)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"

tool_manager = ToolManager()
