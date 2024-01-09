from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
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


class UserToUserGroup(StatesGroup):
    start = State()
    content_type = State()
    genre = State()


@router.message(F.text.casefold() == "просто фильм")
async def select_personal(message: Message, state: FSMContext) -> None:
    """Пользователь выбрал персональную рекомендацию"""

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Показывай уже")]], resize_keyboard=True
    )
    await message.answer("Подборка готова", reply_markup=keyboard)
    await state.set_state(Recommendation.personal)


@router.message(F.text.casefold() == "похожие пользователи")
async def select_user_to_user(
    message: Message, state: FSMContext, user_data: dict
) -> None:
    """Проверяем есть ли данные о типе контента и жанре"""

    if not user_data.get(message.from_user.id) or not user_data.get(
        message.from_user.id
    ).get("user_to_user"):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Фильм"), KeyboardButton(text="Сериал")]],
            resize_keyboard=True,
        )
        await message.answer("Какой контент интересует?", reply_markup=keyboard)
        await state.set_state(UserToUserGroup.content_type)
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Оставить"), KeyboardButton(text="Изменить")]],
            resize_keyboard=True,
        )
        await message.answer(
            f"Данные о вас уже есть:"
            f"\nВид контента: {user_data.get(message.from_user.id).get('user_to_user').get('content_type')}"
            f"\nЖанр: {user_data.get(message.from_user.id).get('user_to_user').get('genre')}",
            reply_markup=keyboard,
        )
        await state.set_state(UserToUserGroup.start)


@router.message(StateFilter(UserToUserGroup.start))
async def reset_content_type(message: Message, state: FSMContext) -> None:
    """Изменить выбранный тип контента"""

    if message.text.lower() == "изменить":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Фильм"), KeyboardButton(text="Сериал")]],
            resize_keyboard=True,
        )
        await message.answer("Какой контент интересует?", reply_markup=keyboard)
        await state.set_state(UserToUserGroup.content_type)
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Показывай уже")]], resize_keyboard=True
        )
        await message.answer("Подборка готова", reply_markup=keyboard)
        await state.set_state(Recommendation.similar_users)


@router.message(StateFilter(UserToUserGroup.content_type))
async def set_content_type(message: Message, state: FSMContext, user_data: dict) -> None:
    """Сохраняем выбранный тип контента"""

    user_data[message.from_user.id] = {"user_to_user": {"content_type": message.text}}

    await state.set_state(UserToUserGroup.genre)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Жанр1"), KeyboardButton(text="Жанр2")]],
        resize_keyboard=True,
    )
    await message.answer("Какой жанр показать?", reply_markup=keyboard)


@router.message(StateFilter(UserToUserGroup.genre))
async def set_genre(message: Message, state: FSMContext, user_data: dict) -> None:
    """Сохраняем выбранный жанр"""

    user_data[message.from_user.id]["user_to_user"]["genre"] = message.text

    await state.set_state(Recommendation.similar_users)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Покажи уже что-нибудь")]], resize_keyboard=True
    )
    await message.answer("Все готово", reply_markup=keyboard)


@router.message(StateFilter(Recommendation.personal))
async def popular(message: Message):
    response = await api.get_personal(message.from_user.id)
    await message.answer(
        f"Фильмы: {response.get('movies')}", reply_markup=ReplyKeyboardRemove()
    )


@router.message(StateFilter(Recommendation.similar_users))
async def user_to_user(message: Message, user_data: dict):
    content_type = user_data[message.from_user.id]["user_to_user"]["content_type"]
    genre = user_data[message.from_user.id]["user_to_user"]["genre"]
    response = await api.get_user_to_user(content_type, genre)
    await message.answer(
        f"Фильмы: {response.get('movies')}", reply_markup=ReplyKeyboardRemove()
    )
