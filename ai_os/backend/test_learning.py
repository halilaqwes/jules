import asyncio
from app.tools.tool_manager import tool_manager
from app.services.memory_service import memory_service
from app.agents.orchestrator import orchestrator

async def test_run():
    # 1. Save a lesson
    res = tool_manager.execute_tool("save_lesson", lesson="Never use single quotes in JSON.")
    print("Tool Execution Result:", res)

    # 2. Check if the prompt injects it correctly
    orchestrator.set_goal("Test learning")

    # Mock
    async def mock_generate(model, prompt, system=""):
        print("\n--- System Prompt Injected ---")
        print(system)
        print("------------------------------\n")
        return "mock"

    from app.services.ollama_service import ollama_service
    ollama_service.generate_response = mock_generate

    await orchestrator._step()

if __name__ == "__main__":
    asyncio.run(test_run())
