from typing import NoReturn
from fastapi import FastAPI, WebSocket
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import vertexai
import vertexai.preview.generative_models as generative_models
from google.oauth2.service_account import Credentials
import os

from src.configs import config
from src.gemini import get_ai_response_async


dir_path = os.path.dirname(os.path.realpath(__file__))
index_path = os.path.join(dir_path, '..', "public", "index.html")
with open(index_path) as f:
    html = f.read()


json_path = os.path.join(dir_path, '..', config.GCP_SERVICE_ACCOUNT_FILENAME)
normalized_json_path = os.path.normpath(json_path)
credentials = Credentials.from_service_account_file(
    normalized_json_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
vertexai.init(credentials=credentials, project=config.GEMINI_PROJECT_NAME, location=config.GEMINI_REGIONS[0])

def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Gemini API with GDG Busan",
        description="Gemini API",
        version="1.0.0",
        docs_url=None if config.APP_ENV == "production" else "/docs",
        redoc_url=None if config.APP_ENV == "production" else "/redoc",
        middleware=make_middleware(),
    )
    return app_


app = create_app()


@app.get("/")
async def web_app() -> HTMLResponse:
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in get_ai_response_async(message):
            await websocket.send_text(text)
