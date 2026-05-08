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
    async def web_search(query: str) -> str:
        """Perform a web search using DuckDuckGo and return results."""
        from ddgs import DDGS
        import asyncio
        try:
            # Run the synchronous DDGS search in an executor to avoid blocking
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, lambda: list(DDGS().text(query, max_results=5)))
            if not results:
                return "No search results found."

            formatted = "Search Results:\n\n"
            for i, res in enumerate(results):
                formatted += f"{i+1}. {res.get('title', 'No Title')}\nURL: {res.get('href', 'No URL')}\nSnippet: {res.get('body', 'No Snippet')}\n\n"
            return formatted
        except Exception as e:
            return f"Search error: {e}"

    @staticmethod
    async def fetch_webpage(url: str) -> str:
        """Fetch the text content of a webpage smartly using Scrapling."""
        from scrapling import Fetcher
        import traceback
        import asyncio

        def run_fetch():
            # Modern Scrapling uses get() to fetch the page
            page = Fetcher.get(url)
            # Find the main body or text
            return page.text

        try:
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(None, run_fetch)

            # Truncate to avoid context explosion
            if len(text) > 10000:
                text = text[:10000] + "\n... [TRUNCATED]"
            return f"Content of {url}:\n\n{text}"
        except Exception as e:
            return f"Error fetching webpage with Scrapling:\n{traceback.format_exc()}"

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
    async def add_external_skill_repo(repo_url: str) -> str:
        """Clone a github repo and install its skills into the AI OS."""
        import tempfile
        import shutil
        import asyncio

        tmp_dir = tempfile.mkdtemp()
        try:
            process = await asyncio.create_subprocess_shell(
                f"git clone {repo_url} {tmp_dir}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

            if process.returncode != 0:
                return f"Error: Failed to clone repository {repo_url}"

            from app.skills.skill_manager import skill_manager
            target_dir = skill_manager.skills_dir

            skills_copied = 0
            for root, dirs, files in os.walk(tmp_dir):
                for file in files:
                    if file.endswith(".md"):
                        src_file = os.path.join(root, file)
                        # We create a unique name based on the path to avoid collisions
                        rel_path = os.path.relpath(src_file, tmp_dir).replace(os.sep, "_")
                        dst_file = os.path.join(target_dir, rel_path)
                        shutil.copy2(src_file, dst_file)
                        skills_copied += 1

            return f"Successfully cloned {repo_url} and integrated {skills_copied} new skills dynamically!"
        except Exception as e:
            return f"Error integrating skill repo: {e}"
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

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

            # Add a longer timeout for heavy operations like git clone or npm install
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300.0)
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return "Command timed out after 300 seconds."

            output = stdout.decode()
            err_output = stderr.decode()
            exit_code = process.returncode

            result_str = f"Exit Code: {exit_code}\n"
            if output:
                result_str += f"STDOUT:\n{output}\n"
            if err_output:
                result_str += f"STDERR:\n{err_output}\n"

            if not output and not err_output and exit_code == 0:
                result_str += "Command executed successfully (no output)."

            return result_str
        except Exception as e:
            return f"Error executing command: {e}"

os_tools = OSTools()
