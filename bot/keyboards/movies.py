from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def movies_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Еще")
    kb.button(text="Что-нибудь похожее на это")
    kb.button(text="Что смотрят такие как я?")
    return kb.as_markup(resize_keyboard=True)
