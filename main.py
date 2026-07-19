from fastapi import FastAPI
from AiAssist.Routers.pdf_router import router as pdf_router
from AiAssist.Routers.question_router import router as user_router
from AiAssist.Routers.summary_router import router as summary_router
from AiAssist.api.middlewares import configure_middleware

app = FastAPI()

# Register middleware
configure_middleware(app)

# Register routers
app.include_router(pdf_router, prefix="/Aurix/api/v1")
app.include_router(user_router,prefix="/Aurix/api/v1")
app.include_router(summary_router,prefix="/Aurix/api/v1")