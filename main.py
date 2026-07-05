from fastapi import FastAPI
from AiAssist.Routers.pdf_router import router as pdf_router
from AiAssist.api.middlewares import configure_middleware

app = FastAPI()

# Register middleware
configure_middleware(app)

# Register routers
app.include_router(pdf_router, prefix="/Aurix/api/v1")