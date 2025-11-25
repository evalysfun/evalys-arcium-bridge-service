"""FastAPI server for Arcium bridge service"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..config.settings import Settings
from ..utils.logger import get_logger
from .routes import router

logger = get_logger(__name__)
settings = Settings()

app = FastAPI(
    title="Evalys Arcium Bridge Service",
    description="Bridge service connecting Evalys to Arcium's encrypted supercomputer",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def root_health():
    """Root-level health check endpoint"""
    return {"status": "healthy", "service": "evalys-arcium-bridge"}


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info(f"Starting Evalys Arcium Bridge Service on {settings.api_host}:{settings.api_port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down Evalys Arcium Bridge Service")


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
    )

