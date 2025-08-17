from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1.products import router as products_router
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(_: FastAPI):
    if os.getenv("ENV", "DEV") == "DEV":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(products_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}






