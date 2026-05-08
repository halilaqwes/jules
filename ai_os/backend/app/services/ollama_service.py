import httpx
import json
from typing import List, Dict, Any

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def list_models(self) -> List[Dict[str, Any]]:
        """List all available local Ollama models."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                return data.get("models", [])
            except Exception as e:
                print(f"Error fetching models: {e}")
                return []

    async def generate_response(self, model: str, prompt: str, system: str = "") -> str:
        """Generate a single response from the model."""
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "system": system,
                    "stream": False
                }
                response = await client.post(f"{self.base_url}/api/generate", json=payload, timeout=120.0)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except Exception as e:
                print(f"Error generating response: {e}")
                return f"Error: {str(e)}"

    async def stream_response(self, model: str, prompt: str, system: str = ""):
        """Stream a response from the model (Generator)."""
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "system": system,
                    "stream": True
                }
                async with client.stream("POST", f"{self.base_url}/api/generate", json=payload, timeout=120.0) as response:
                    async for chunk in response.aiter_lines():
                        if chunk:
                            try:
                                data = json.loads(chunk)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                pass
            except Exception as e:
                yield f"\n[Error streaming response: {str(e)}]"

ollama_service = OllamaService()
