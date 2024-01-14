from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.data import (
    age_select_keyboard,
    gender_select_keyboard,
    income_select_keyboard,
    kids_select_keyboard,
)
from keyboards.general import start_keyboard
from utils.db import set_age, set_income, set_kids, set_sex


router = Router()


class User(StatesGroup):
    age = State()
    income = State()
    sex = State()
    kids = State()
    user_filled = State()


@router.message(StateFilter(User.age))
async def age(message: Message, state: FSMContext):

    await state.set_state(User.income)
    await message.answer("Укажите возраст", reply_markup=age_select_keyboard())


@router.message(StateFilter(User.income))
async def income(message: Message, state: FSMContext):

    set_age(message.from_user.id, message.text.lower())

    await state.set_state(User.sex)
    await message.answer("Укажите доход", reply_markup=income_select_keyboard())


@router.message(StateFilter(User.sex))
async def sex(message: Message, state: FSMContext):

    set_income(message.from_user.id, message.text.lower())

    await state.set_state(User.kids)
    await message.answer("Укажите пол", reply_markup=gender_select_keyboard())


@router.message(StateFilter(User.kids))
async def kids(message: Message, state: FSMContext):
    set_sex(message.from_user.id, message.text.lower())

    await state.set_state(User.user_filled)
    await message.answer("Есть ли у вас дети?", reply_markup=kids_select_keyboard())


@router.message(StateFilter(User.user_filled))
async def finish_user_data(message: Message, state: FSMContext):
    set_kids(message.from_user.id, message.text.lower())

    await message.answer(
        "Спасибо, теперь можно перейти к фильмам", reply_markup=start_keyboard()
    )
    await state.clear()
