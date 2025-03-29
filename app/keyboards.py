from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Как загрузить excel-файл")
    kb.button(text="Вывести среднюю цену на товар")
    kb.button(text="Обзор базы данных")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
