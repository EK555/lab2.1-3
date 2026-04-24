from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import services
from app.api.routes import auth
from app.core.config import settings

# Создаем приложение
app = FastAPI(
    title="SPA Salon API",
    version="1.0.0",
    debug=settings.ENVIRONMENT == "development"  
)

#  НАСТРОЙКИ CORS для работы с cookies 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,   # ВАЖНО: разрешаем cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router, prefix="/api/v1")

# РОУТЫ для аутентификации
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "SPA Salon API", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}