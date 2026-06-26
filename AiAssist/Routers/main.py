from fastapi import FastAPI
from Routers.FileMetadataRouter import router

app = FastAPI()

app.include_router(router)