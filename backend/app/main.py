"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import init_database
from backend.app.routers import (
    experiment,
    funnel,
    health,
    model,
    nba,
    overview,
    retention,
    users,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the application database on startup."""
    init_database()
    yield


app = FastAPI(
    title="Career Growth Analytics Enterprise API",
    description="Enterprise-level API for AI Career Platform growth analytics.",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(overview.router)
app.include_router(funnel.router)
app.include_router(retention.router)
app.include_router(experiment.router)
app.include_router(model.router)
app.include_router(users.router)
app.include_router(nba.router)


@app.get("/")
def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": "Career Growth Analytics Enterprise API",
        "version": "0.3.0",
        "docs": "/docs",
    }
