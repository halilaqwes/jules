import asyncio
from app.agents.orchestrator import orchestrator
from app.tools.tool_manager import tool_manager
from app.services.memory_service import memory_service

async def test_run():
    print("Available Tools:", tool_manager.get_available_tools_description())

    # Simulate setting a goal
    orchestrator.set_goal("Write a python script that prints hello world to hello.py")

    # We step the orchestrator manually
    print("\nRunning one step of orchestrator...")
    # NOTE: In a real environment, the orchestrator needs an Ollama model running.
    # Since Ollama might not be running in this sandbox, we will mock the response for the test

    # Mock
    async def mock_generate(*args, **kwargs):
        return """
Thinking: I need to write a file.
```json
{
  "tool": "write_file",
  "args": {
    "filepath": "hello.py",
    "content": "print('hello world')"
  }
}
```
"""
    from app.services.ollama_service import ollama_service
    ollama_service.generate_response = mock_generate

    await orchestrator._step()

    print("\nChecking memory logs after step:")
    logs = memory_service.get_recent_events("orchestrator", limit=3)
    for log in logs:
        print(f"[{log['event_type']}] {log['content']}")

    print("\nChecking if file was written:")
    import os
    if os.path.exists("hello.py"):
        with open("hello.py", "r") as f:
            print("hello.py content:", f.read())
        os.remove("hello.py")
    else:
        print("File was not written.")

if __name__ == "__main__":
    asyncio.run(test_run())
