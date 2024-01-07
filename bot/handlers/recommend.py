from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from utils.recsys_api import RecsysAPI


markup_text = "<b>Фильм:</b> {}\n\nГод выпуска: {}\n\nЖанры: {}\n\n\n{}"

router = Router()
api = RecsysAPI()


class Recommendation(StatesGroup):
    popular = State()
    personal = State()
    similar_movies = State()
    similar_users = State()
    end = State()


@router.message(StateFilter(Recommendation.popular))
async def popular(message: Message):
    response = await api.get_popular()
    await message.answer(
        f"Фильмы: {response.get('movies')}", reply_markup=ReplyKeyboardRemove()
    )
