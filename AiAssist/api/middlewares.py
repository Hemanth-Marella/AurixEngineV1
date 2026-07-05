from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..Routers.pdf_router import router as pdf_router


app = FastAPI()

origins = [
    'https://aurix-engine-study-helper-ai.netlify.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(pdf_router, prefix="/Aurix/api/v1")