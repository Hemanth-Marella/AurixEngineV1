from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def configure_middleware(app: FastAPI):
    origins = [
        "https://aurix-engine-study-helper-ai.netlify.app"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )