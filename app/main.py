from fastapi import FastAPI
from contextlib import asynccontextmanager
# from app.database import engine
# from app.models import Base
from app.api import auth, users, admin, webhook
from app.migrations.initial_data import create_initial_data
from app.database import AsyncSessionLocal, Base, engine


@asynccontextmanager
async def lifespan(app_f: FastAPI):
    # Создаем таблицы при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем начальные данные
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        from app.models import User

        result = await db.execute(select(User).limit(1))
        if not result.scalar_one_or_none():
            await create_initial_data(db)

    yield

    # Cleanup при завершении
    await engine.dispose()


app = FastAPI(
    title="Payment System API",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(webhook.router)


@app.get("/")
async def root():
    return {"message": "Payment System API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
