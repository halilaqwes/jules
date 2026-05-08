import os
import subprocess
from typing import Dict, Any

class OSTools:
    """Built-in OS capabilities for the agent."""

    @staticmethod
    def read_file(filepath: str) -> str:
        """Read a file from disk and provide a summary if it's too large."""
        import os
        try:
            if not os.path.exists(filepath):
                return f"Error: File '{filepath}' does not exist."

            # If file is too large (e.g., > 50KB), we truncate it so we don't blow up context limit
            file_size = os.path.getsize(filepath)
            MAX_SIZE = 50 * 1024 # 50 KB

            with open(filepath, 'r', encoding='utf-8') as f:
                if file_size > MAX_SIZE:
                    content = f.read(MAX_SIZE)
                    return f"--- FILE IS LARGE (Truncated to first 50KB for analysis) ---\n{content}\n... [TRUNCATED]"
                else:
                    return f.read()
        except UnicodeDecodeError:
            return f"Error: File '{filepath}' appears to be a binary file or non-UTF-8 text."
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
    def open_browser_url(url: str) -> str:
        """Open a URL in the system's default web browser."""
        import webbrowser
        try:
            success = webbrowser.open(url)
            if success:
                return f"Successfully opened {url} in the browser."
            else:
                return f"Failed to open {url} in the browser."
        except Exception as e:
            return f"Error opening browser: {e}"

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
