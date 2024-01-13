from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def movies_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Еще")
    kb.button(text="Хватит")
    kb.button(text="Похожий на этот")
    return kb.as_markup(resize_keyboard=True)


def show_movies_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Показывай")
    return kb.as_markup(resize_keyboard=True)
