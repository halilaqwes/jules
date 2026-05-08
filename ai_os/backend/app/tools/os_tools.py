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
    async def run_bash(command: str) -> str:
        """Run a bash command asynchronously and return output."""
        import asyncio
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Add a timeout manually since create_subprocess_shell doesn't have it built-in
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30.0)
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return "Command timed out."

            output = stdout.decode()
            err_output = stderr.decode()

            if err_output:
                output += f"\nSTDERR:\n{err_output}"

            return output if output else "Command executed successfully (no output)."
        except Exception as e:
            return f"Error executing command: {e}"

os_tools = OSTools()
