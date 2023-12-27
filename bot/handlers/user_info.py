from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router, F
from aiogram.types import Message

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.db import set_age, set_sex, set_income, set_kids

router = Router()


class User(StatesGroup):
    age = State()
    income = State()
    sex = State()
    kids = State()
    user_filled = State()


@router.message(StateFilter(User.age))
async def age(message: Message, state: FSMContext):
    buttons = [[KeyboardButton(text="18-24"), KeyboardButton(text="25-34"), KeyboardButton(text="35-44"),
                KeyboardButton(text="45-54"), KeyboardButton(text="55-64"), KeyboardButton(text="65+"),
                KeyboardButton(text="Не отвечать")]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await state.set_state(User.income)
    await message.answer("Укажите возраст", reply_markup=keyboard)


@router.message(StateFilter(User.income))
async def income(message: Message, state: FSMContext):
    set_age(message.from_user.id, message.text.lower())
    buttons = [[KeyboardButton(text="0-20к"), KeyboardButton(text="20-40к"), KeyboardButton(text="40-60к"),
                KeyboardButton(text="60-90к"), KeyboardButton(text="90-150к"), KeyboardButton(text="150к+"),
                KeyboardButton(text="Не отвечать")]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await state.set_state(User.sex)
    await message.answer("Укажите доход", reply_markup=keyboard)


@router.message(StateFilter(User.sex))
async def sex(message: Message, state: FSMContext):
    set_income(message.from_user.id, message.text.lower())
    buttons = [[KeyboardButton(text="м"), KeyboardButton(text="ж"), KeyboardButton(text="Не отвечать")]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await state.set_state(User.kids)
    await message.answer("Укажите пол", reply_markup=keyboard)


@router.message(StateFilter(User.kids))
async def kids(message: Message, state: FSMContext):
    set_sex(message.from_user.id, message.text.lower())
    buttons = [[KeyboardButton(text="Да"), KeyboardButton(text="Нет"), KeyboardButton(text="Не отвечать")]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await state.set_state(User.user_filled)
    await message.answer("Есть ли у вас дети?", reply_markup=keyboard)


@router.message(StateFilter(User.user_filled))
async def finish_user_data(message: Message, state: FSMContext):
    set_kids(message.from_user.id, message.text.lower())
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поехали")]], resize_keyboard=True)

    await message.answer("Спасибо, теперь можно перейти к фильмам", reply_markup=keyboard)
    await state.clear()
