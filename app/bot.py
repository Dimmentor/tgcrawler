import logging
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from sqlalchemy import select

from app.config import settings
from app.file_handlers import handle_excel, sources_getter
from app.keyboards import main_keyboard
from app.database import async_session_maker
from app.models import Source
from app.crawler import get_average_price

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Приветствую! Я вывожу цены в книжных магазинах и высчитываю среднюю цену на книгу 'Гарри Поттер и Философский камень'.",
                         reply_markup=main_keyboard())


@dp.message(F.text == "Как загрузить excel-файл")
async def cmd_upload(message: types.Message):
    await message.answer("Для того, чтобы загрузить Excel-файл, нажмите на иконку скрепки и далее Document.")


@dp.message(F.text == "Обзор базы данных")
async def cmd_get_table(message: types.Message):
    async with async_session_maker() as session:
        sources = await sources_getter(session)

        if not sources:
            await message.answer("В базе данных пока нет записей.")
            return

        response_message = "Список источников:\n"
        for index, source in enumerate(sources, start=1):
            response_message += f"{index}) {source.title}\n"

        await message.answer(response_message)


@dp.message(F.text == "Вывести среднюю цену на товар")
async def get_prices(message: types.Message):
    await message.answer("Ожидайте, загрузка цен займет некоторое время...")
    start_time = time.time()

    async with async_session_maker() as session:
        sources = await session.execute(select(Source))
        sources = sources.scalars().all()

        if not sources:
            await message.answer("Ошибка: В базе данных пока нет записей")
            return

        results, average_price = await get_average_price(sources)

    end_time = time.time()
    elapsed_time = end_time - start_time

    response_message = "\n".join(results) + f"\nСредняя цена на товары: {int(average_price)} р."
    response_message += f"\nВремя выполнения операции: {elapsed_time:.2f} секунд."  # Добавляем время выполнения
    await message.answer(response_message)


@dp.message(F.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
async def handle_excel_sender(message: types.Message):
    async with async_session_maker() as session:
        await handle_excel(message, bot, session)


async def start_bot():
    await dp.start_polling(bot)
