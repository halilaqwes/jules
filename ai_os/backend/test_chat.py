import asyncio
from app.agents.orchestrator import orchestrator

async def test_run():
    print("Testing chat response...")

    # Mock Ollama generate for chat
    async def mock_generate(model, prompt, system=""):
        print("\n--- System Prompt ---")
        print(system[:200] + "...")
        print("\n--- Chat Prompt ---")
        print(prompt)
        print("-------------------\n")
        return "Hello! How can I help you code today?"

    from app.services.ollama_service import ollama_service
    ollama_service.generate_response = mock_generate

    res = await orchestrator.handle_chat_message("Hi, are you there?")
    print("Agent Response:", res)
    print("Chat History:", orchestrator.chat_history)

if __name__ == "__main__":
    asyncio.run(test_run())
