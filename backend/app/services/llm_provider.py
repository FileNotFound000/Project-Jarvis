from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    async def configure(self, settings: Dict[str, Any]):
        """
        Configures the provider with the given settings.
        """
        pass

    @abstractmethod
    async def send_message_stream(
        self, 
        history: List[Dict[str, str]], 
        message: str, 
        images: List[bytes] = None
    ) -> AsyncGenerator[str, None]:
        """
        Sends a message to the model and yields text chunks.
        
        Args:
            history: List of message dicts [{"role": "user"|"model", "content": "..."}]
            message: The new user message string.
            images: Optional list of image bytes.
            
        Yields:
            str: Text chunks of the response.
        """
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding vector for the given text.
        """
        pass
