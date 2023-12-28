import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.db import check_user, is_user_filled
from handlers import user_info, recommendations
from handlers.user_info import User
from handlers.recommendations import Recommendation

TOKEN = '6899841169:AAHfbiQQR_kOtiLEBqtzX-HbnPhizp5myME'  # TODO унести отсюда

dp = Dispatcher()

user_data = {}

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
        await state.set_state(Recommendation.popular)
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поехали")]], resize_keyboard=True)
        await message.answer("Посоветовать фильм?", reply_markup=keyboard)


@dp.message(F.text.casefold() == "поехали")
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    """Проверяем заполнены ли у пользователя данные в БД и от этого решаем что покказать"""

    filled = is_user_filled(message.from_user.id)
    if filled:
        await state.set_state(Recommendation.popular)
    else:
        await state.set_state(Recommendation.popular)

    buttons = [[KeyboardButton(text="Посоветуй фильм")]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Что делаем?", reply_markup=keyboard)


async def main() -> None:

    dp.include_routers(user_info.router, recommendations.router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
