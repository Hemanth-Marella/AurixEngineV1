from fastapi import FastAPI
from AiAssist.Routers.pdf_router import router

app = FastAPI()

app.include_router(router)