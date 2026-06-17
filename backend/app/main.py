"""FastAPI 应用入口。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import get_connection, init_database
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


def _database_is_empty() -> bool:
    """Check whether the SQLite database has been seeded."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时初始化本地数据库，若为空则自动 seed。"""
    init_database()
    if _database_is_empty():
        from backend.app.services.data_service import seed_database

        seed_database()
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
    """返回 API 基础信息的根接口。"""
    return {
        "name": "Career Growth Analytics Enterprise API",
        "version": "0.3.0",
        "docs": "/docs",
    }
