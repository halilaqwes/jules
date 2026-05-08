import os
import subprocess
from typing import Dict, Any

class OSTools:
    """Built-in OS capabilities for the agent."""

    @staticmethod
    def read_file(filepath: str) -> str:
        """Read a file from disk."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    @staticmethod
    def write_file(filepath: str, content: str) -> str:
        """Write content to a file on disk."""
        try:
            dir_name = os.path.dirname(filepath)
            if dir_name:  # Only create directory if it's not the current directory
                os.makedirs(dir_name, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing file: {e}"

    @staticmethod
    def run_bash(command: str) -> str:
        """Run a bash command and return output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            return output if output else "Command executed successfully (no output)."
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except Exception as e:
            return f"Error executing command: {e}"

os_tools = OSTools()
