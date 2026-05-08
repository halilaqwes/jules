import asyncio
from app.tools.tool_manager import tool_manager

async def test():
    # Write a dummy python file
    tool_manager.execute_tool = tool_manager.execute_tool
    res = await tool_manager.execute_tool("write_file", filepath="test.py", content="import time\ntime.sleep(1)\nprint('async success')")
    print("Write file:", res)

    # Run bash async
    print("Running bash async...")
    res = await tool_manager.execute_tool("run_bash", command="python test.py")
    print("Bash result:", res)

    # Cleanup
    import os
    os.remove("test.py")

asyncio.run(test())
