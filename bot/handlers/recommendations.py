import requests
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove


markup_text = "<b>Фильм:</b> {}\n\nГод выпуска: {}\n\nЖанры: {}\n\n\n{}"

router = Router()


class Recommendation(StatesGroup):
    popular = State()
    personal = State()
    similar_movies = State()
    similar_users = State()
    end = State()


@router.message(StateFilter(Recommendation.popular))
async def popular(message: Message, state: FSMContext):
    response = requests.get("http://recsys-service:8000/popular")
    await message.answer(
        f"Фильмы: {response.json().get('movies')}", reply_markup=ReplyKeyboardRemove()
    )
