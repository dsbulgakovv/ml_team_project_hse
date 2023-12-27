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
from utils.db import check_user
from handlers import user_info
from handlers.user_info import User, age

TOKEN = '6899841169:AAHfbiQQR_kOtiLEBqtzX-HbnPhizp5myME'  # TODO унести отсюда

dp = Dispatcher()

markup_text = "<b>Фильм:</b> {}\n\nГод выпуска: {}\n\nЖанры: {}\n\n\n{}"

user_data = {}

router = Router()


class Form(StatesGroup):
    movie_choice = State()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    """This handler receives messages with `/start` command"""

    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")
    new_user = check_user(message.from_user.id)
    if new_user:
        buttons = [[KeyboardButton(text="Да"), KeyboardButton(text="Почему бы и нет")]]
        keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer("Поделитесь данными о себе", reply_markup=keyboard)
        await state.set_state(User.age)


@dp.message(Form.movie_choice, F.text.casefold() == "посоветуй фильм")
async def command_start_handler(message: types.Message) -> None:
    """This handler receives request to show next movie"""

    if message.from_user.id not in user_data:
        user_data[message.from_user.id] = [1, 2, 3]
    movie = next(user_data[message.from_user.id], None)
    print(movie)
    if movie:
        response = markup_text.format(movie.get('title'), int(movie.get('release_year')),
                                      movie.get('genres'), movie.get('description'))
        await message.answer(response)
    else:
        await message.answer('Для вас фильмы кончились :(', reply_markup=ReplyKeyboardRemove())


@dp.message(Form.movie_choice, F.text.casefold() == "остановитесь")
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    """This handler receives request to stop sending movies"""

    await state.clear()
    await message.answer('Ок, заканчиваю', reply_markup=ReplyKeyboardRemove())


#@dp.message()
#async def echo_handler(message: types.Message) -> None:
#    """ Forward received message back to the sender"""
#    try:
#        await message.send_copy(chat_id=message.chat.id)
#    except TypeError:
#        await message.answer("Nice try!")


async def main() -> None:

    dp.include_routers(user_info.router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
