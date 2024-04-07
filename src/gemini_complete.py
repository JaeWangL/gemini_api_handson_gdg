from typing import AsyncGenerator
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel, Part


async def get_ai_response_async(message: str, stream: bool=True) -> AsyncGenerator[str, None]:
    model_vision = GenerativeModel("gemini-1.0-pro-vision-001")
    # image = Part.from_uri('gs://mathtest3/101_1.png', problem_image_mime_type)
    response = await model_vision.generate_content_async(
        [message],
        generation_config={
            "max_output_tokens": 2048,
            "stop_sequences": [
                "###"
            ],
            "temperature": 0,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        stream=stream,
    )

    all_content = ""
    async for chunk in response:
        content = chunk.text
        if content:
            all_content += content
            yield all_content