from typing import AsyncGenerator
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel, Part


async def gemini_async(message: str, stream: bool=True) -> AsyncGenerator[str, None]:
    yield "Hello World"
