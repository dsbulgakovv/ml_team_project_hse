from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from constraints.genres import genres


def share_data_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Почему бы и нет")
    return kb.as_markup(resize_keyboard=True)


def age_select_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="18-24")
    kb.button(text="25-34")
    kb.button(text="35-44")
    kb.button(text="45-54")
    kb.button(text="55-64")
    kb.button(text="65+")
    kb.button(text="Не отвечать")

    return kb.as_markup(resize_keyboard=True)


def income_select_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="0-20к")
    kb.button(text="20-40к")
    kb.button(text="40-60к")
    kb.button(text="60-90к")
    kb.button(text="90-150к")
    kb.button(text="150к+")
    kb.button(text="Не отвечать")

    return kb.as_markup(resize_keyboard=True)


def gender_select_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мужчина")
    kb.button(text="Женщина")
    kb.button(text="Не отвечать")

    return kb.as_markup(resize_keyboard=True)


def kids_select_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.button(text="Не отвечать")

    return kb.as_markup(resize_keyboard=True)


def edit_preferences_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Оставить")
    kb.button(text="Изменить")

    return kb.as_markup(resize_keyboard=True)


def content_type_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Фильм")
    kb.button(text="Сериал")

    return kb.as_markup(resize_keyboard=True)


def genres_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for genre in genres:
        kb.button(text=genre)
    return kb.as_markup(resize_keyboard=True)
