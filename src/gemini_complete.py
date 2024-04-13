import base64
from typing import AsyncGenerator
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel, Part


async def gemini_async(prompt: str, stream: bool=True) -> AsyncGenerator[str, None]:
    model_vision = GenerativeModel("gemini-1.0-pro-vision-001")
    response = await model_vision.generate_content_async([
        f"instruction: {prompt}",
        ],
        generation_config={
            "max_output_tokens": 2048,
            "stop_sequences": [
                "###"
            ],
            "temperature": 0.7,
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


async def gemini_with_image_async(prompt: str, image_gcs: str|None=None, image_base64_encoded: bytes|None=None, stream: bool=True) -> AsyncGenerator[str, None]:
    model_vision = GenerativeModel("gemini-1.0-pro-vision-001")
    if image_gcs is not None:
        image = Part.from_uri(image_gcs, mime_type="image/png")
    else:
        image = Part.from_data(
            data=base64.b64decode(image_base64_encoded),
            mime_type="image/png"
        )
    response = await model_vision.generate_content_async(
        [
            "Image1: ", image,
            "Image2: ", image,
            "Instruction:", prompt
        ],
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


async def gemini_with_video_async(prompt: str, video_gcs: str|None=None, video_base64_encoded: bytes|None=None, stream: bool=True) -> AsyncGenerator[str, None]:
    model_vision = GenerativeModel("gemini-1.0-pro-vision-001")
    if video_gcs is not None:
        video = Part.from_uri(video_gcs, mime_type="video/mp4")
    else:
        video = Part.from_data(
            data=base64.b64decode(video_base64_encoded),
            mime_type="video/mp4"
        )
    response = await model_vision.generate_content_async(
        [video, prompt],
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