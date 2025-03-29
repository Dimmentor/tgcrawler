import os
import pandas as pd
from aiogram import types
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.validators import validate_source_data, check_entry
from app.models import Source


async def handle_excel(message: types.Message, bot: Bot, session: AsyncSession):
    file = await bot.get_file(message.document.file_id)
    destination_file = f'app/files/{message.document.file_name}'
    await bot.download_file(file.file_path, destination_file)

    try:
        if not destination_file.endswith(('.xls', '.xlsx')):
            await message.answer("Ошибка: Загруженный файл не является Excel файлом.")
            return

        df = pd.read_excel(destination_file, header=None) #без заголовка

        if df.shape[1] != 3:
            await message.answer("Ошибка: Неверное содержание файла. Ожидается 3 колонки.")
            return

        not_added = []

        for index, row in df.iterrows():
            title, url, xpath = row.iloc[0], row.iloc[1], row.iloc[2]
            validation_error = await validate_source_data(title, url, xpath)
            if validation_error:
                not_added.append(f"{title} не был добавлен в базу данных, причина: {validation_error}")
                continue

            existing_entry = await check_entry(session, title, url, xpath)
            if existing_entry:
                not_added.append(
                    f"{title} не был добавлен в базу данных\nПричина: одно из значений в файле уже есть в базе данных.")
                continue

            await add_source_to_db(session, title, url, xpath)
            await message.answer(f"Сайт успешно добавлен в БД: {title}, {url}, {xpath}")

        if not_added:
            await message.answer("\n".join(not_added))

    except Exception as e:
        await message.answer("Произошла ошибка при обработке файла: " + str(e))

    finally:
        if os.path.exists(destination_file):
            os.remove(destination_file)


async def add_source_to_db(session: AsyncSession, title: str, url: str, xpath: str):
    new_source = Source(title=title, url=url, xpath=xpath)
    session.add(new_source)
    await session.commit()


async def sources_getter(session):
    result = await session.execute(select(Source))
    sources = result.scalars().all()
    return sources