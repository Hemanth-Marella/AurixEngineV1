from fastapi import FastAPI
from AiAssist.Routers.DocumentMetadataRouter import router

app = FastAPI()

app.include_router(router)