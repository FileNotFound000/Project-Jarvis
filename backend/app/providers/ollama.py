import requests
import json
from typing import AsyncGenerator, List, Dict, Any
from app.services.llm_provider import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "llama3"

    async def configure(self, settings: Dict[str, Any]):
        provider_settings = settings.get("providers", {}).get("ollama", {})
        self.base_url = provider_settings.get("base_url", "http://localhost:11434")
        self.model = provider_settings.get("model", "llama3")
        self.system_instruction = settings.get("system_instruction")

    async def send_message_stream(
        self, 
        history: List[Dict[str, str]], 
        message: str, 
        images: List[bytes] = None
    ) -> AsyncGenerator[str, None]:
        
        # Prepare messages
        messages = []
        
        # Add system instruction if available
        if hasattr(self, 'system_instruction') and self.system_instruction:
            messages.append({"role": "system", "content": self.system_instruction})
            
        for msg in history:
            role = "user" if msg["role"] == "user" else "assistant"
            # Ollama expects 'assistant' not 'model'
            messages.append({"role": role, "content": msg["content"]})
            
        # Add current message
        current_msg = {"role": "user", "content": message}
        if images:
            # Ollama supports images in 'images' field (list of base64 strings usually, 
            # but let's check API. It expects 'images' as list of base64 encoded strings)
            import base64
            encoded_images = []
            for img_bytes in images:
                encoded_images.append(base64.b64encode(img_bytes).decode('utf-8'))
            current_msg["images"] = encoded_images
            
        messages.append(current_msg)

        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.7,
                "num_ctx": 4096,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        }
        
        # DEBUG: Log the messages being sent
        print(f"DEBUG: Sending messages to Ollama: {json.dumps(messages, indent=2)}")

        try:
            # Use requests with stream=True
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        try:
                            json_response = json.loads(line.decode('utf-8'))
                            if "message" in json_response and "content" in json_response["message"]:
                                content = json_response["message"]["content"]
                                yield content
                            
                            if json_response.get("done", False):
                                break
                        except json.JSONDecodeError:
                            print(f"Failed to decode JSON from Ollama: {line}")
                            continue
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            yield f"Error communicating with Ollama: {str(e)}"

    async def get_embedding(self, text: str) -> List[float]:
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model, # Use the same model or a specific embedding model? 
                                 # Ideally "nomic-embed-text" or "mxbai-embed-large" but "llama3" works too usually.
            "prompt": text
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [])
        except Exception as e:
            print(f"Error generating embedding with Ollama: {e}")
            return []
