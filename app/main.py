import asyncio
from fastapi import FastAPI

from app.bot import start_bot, bot
from app.database import engine, Base
from app.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Системное сообщение: Бот запущен')
    await bot.send_message(settings.ADMIN_ID, 'Системное сообщение: Бот запущен')

    asyncio.create_task(start_bot())


@app.on_event("shutdown")
async def shutdown():
    await bot.send_message(settings.ADMIN_ID, 'Системное сообщение: Бот остановлен')
    print('Системное сообщение: Бот остановлен')
    await engine.dispose()

# uvicorn app.main:app --reload
