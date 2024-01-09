import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold
from handlers import recommend, user_info
from handlers.user_info import User
from utils.db import check_user


TOKEN = "token"  # TODO унести отсюда

dp = Dispatcher()
dp["user_data"] = {}

router = Router()


class Form(StatesGroup):
    movie_choice = State()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    """Наполняем данные о пользователе если он новый, иначе сразу предлагаем фильм"""

    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")
    new_user = check_user(message.from_user.id)
    if new_user:
        buttons = [[KeyboardButton(text="Да"), KeyboardButton(text="Почему бы и нет")]]
        keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer("Поделитесь данными о себе", reply_markup=keyboard)
        await state.set_state(User.age)
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Поехали")]], resize_keyboard=True
        )
        await message.answer("Посоветовать фильм?", reply_markup=keyboard)


@dp.message(F.text.casefold() == "поехали")
async def start_recommendations(message: types.Message) -> None:
    """Проверяем заполнены ли у пользователя данные в БД и от этого решаем что показать"""

    buttons = [
        [KeyboardButton(text="Просто фильм"), KeyboardButton(text="Похожие пользователи")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Что показать?", reply_markup=keyboard)


async def main() -> None:

    dp.include_routers(user_info.router, recommend.router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
