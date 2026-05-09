import json
import inspect
from typing import Callable, Dict, Any, List
from .os_tools import os_tools
from .oracle_tools import oracle_tools

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        self.register("read_file", os_tools.read_file, "Read the contents of a file. Args: filepath (str)")
        self.register("write_file", os_tools.write_file, "Write contents to a file. Args: filepath (str), content (str)")
        self.register("run_bash", os_tools.run_bash, "Run a bash command. Args: command (str)")
        self.register("open_browser_url", os_tools.open_browser_url, "Open a URL in the system's default web browser. Args: url (str)")
        self.register("web_search", os_tools.web_search, "Perform a web search to find information, docs, or solutions. Args: query (str)")
        self.register("fetch_webpage", os_tools.fetch_webpage, "Fetch and read the text content of a specific webpage URL. Args: url (str)")
        self.register("add_external_skill_repo", os_tools.add_external_skill_repo, "Clone a github repo url and install its .md skill files into the AI OS memory dynamically. Args: repo_url (str)")

        self.register("ask_deepseek_oracle", oracle_tools.ask_deepseek_oracle, "Escalation Tool: Use this ONLY when you are stuck and cannot resolve an error after multiple attempts. It submits your context to a higher-intelligence Oracle model via web interface to get the correct code/fix. Args: query (str)")

        self.register("create_custom_tool", self.create_custom_tool, "Write a new python tool for the AI OS and dynamically load it. Args: tool_name (str), description (str), python_code (str - Must define an async function with the same name as tool_name)")

        # Load any previously created custom tools
        self._load_custom_tools()

    def _load_custom_tools(self):
        import os
        import importlib.util
        import sys

        custom_tools_dir = os.path.join(os.path.dirname(__file__), "custom")
        if not os.path.exists(custom_tools_dir):
            return

        for file in os.listdir(custom_tools_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                file_path = os.path.join(custom_tools_dir, file)
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    if hasattr(module, "register_tool"):
                        module.register_tool(self)
                except Exception as e:
                    print(f"Failed to load custom tool {file}: {e}")
        self.register("delegate_task", lambda **kwargs: "Async handled by orchestrator",
                      "Delegate a specific task to a sub-agent. Args: agent_type (str: 'tester' or 'researcher'), task_description (str)")

        self.register("save_lesson", self._save_lesson, "Save a lesson learned from a mistake or success to memory. Args: lesson (str)")

    def create_custom_tool(self, tool_name: str, description: str, python_code: str) -> str:
        """Saves python code to custom tools dir and dynamically loads it."""
        import os
        import importlib.util
        import sys

        custom_tools_dir = os.path.join(os.path.dirname(__file__), "custom")
        os.makedirs(custom_tools_dir, exist_ok=True)

        file_path = os.path.join(custom_tools_dir, f"{tool_name}.py")

        # Write the wrapper that auto-registers it
        wrapped_code = f"""
{python_code}

def register_tool(manager):
    manager.register("{tool_name}", {tool_name}, "{description}")
"""
        try:
            import py_compile
            import traceback
            # 1. First, compile the code to check for SyntaxErrors before writing
            try:
                py_compile.compile(file_path, doraise=True) # Will fail since file doesn't exist yet, so we compile string
            except Exception:
                pass # Handled below by compile string

            try:
                compile(wrapped_code, f"{tool_name}_virtual.py", "exec")
            except SyntaxError as e:
                err_msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                return f"SyntaxError in your generated code. Please fix it and try again:\n{err_msg}"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(wrapped_code)

            # 2. Dynamically load the new module
            spec = importlib.util.spec_from_file_location(tool_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[tool_name] = module

            try:
                spec.loader.exec_module(module)
            except Exception as e:
                # If execution/import fails (e.g. ModuleNotFoundError inside the code)
                err_msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                os.remove(file_path) # Cleanup broken file
                return f"Runtime Error while loading your module. Did you import a missing package? Fix and retry:\n{err_msg}"

            if hasattr(module, "register_tool"):
                module.register_tool(self)
                return f"Successfully created and loaded custom tool '{tool_name}'!"
            return "Tool file written, but failed to find register_tool hook."
        except Exception as e:
            import traceback
            return f"Error creating custom tool:\n{traceback.format_exc()}"

    def _save_lesson(self, lesson: str) -> str:
        from app.services.memory_service import memory_service
        lessons = memory_service.get_memory("learned_lessons") or []
        if lesson not in lessons:
            lessons.append(lesson)
            memory_service.set_memory("learned_lessons", lessons)
            return f"Lesson successfully saved: {lesson}"
        return "Lesson already exists in memory."

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

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name with the given arguments."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."

        func = self.tools[tool_name]["function"]
        try:
            import inspect
            if inspect.iscoroutinefunction(func):
                return await func(**kwargs)
            else:
                return func(**kwargs)
        except TypeError as e:
            if "mapping" in str(e).lower() or "unexpected keyword argument" in str(e).lower() or "missing" in str(e).lower():
                return f"Error executing tool '{tool_name}': {e}. Ensure 'args' is a JSON object with correct keys matching the tool's required parameters."
            return f"Error executing tool '{tool_name}': {e}"
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"

tool_manager = ToolManager()
