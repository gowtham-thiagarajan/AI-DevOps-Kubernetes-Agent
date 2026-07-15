from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from api.routes.health import router as health_router
from api.routes.investigation import router as investigation_router
from api.routes.auth import router as auth_router
from api.routes.clusters import router as clusters_router
from core.config import settings
from core.logging import setup_logging
from db import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    logger.info("AI Kubernetes Agent backend starting")
    yield
    logger.info("AI Kubernetes Agent backend shutting down")


app = FastAPI(
    title="AI Kubernetes Agent",
    description="On-demand Kubernetes troubleshooting with AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(investigation_router)
app.include_router(auth_router)
app.include_router(clusters_router)
