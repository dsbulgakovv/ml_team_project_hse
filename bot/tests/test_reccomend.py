import pytest
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from handlers.recommend import (
    UserToUserGroup,
    reset_content_type,
    select_personal,
    select_user_to_user,
)


@pytest.mark.asyncio
async def test_select_personal():
    request = MockedBot(MessageHandler(select_personal))
    calls = await request.query(
        message=MESSAGE.as_object(text="Просто фильм"), user_data={}
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Подборка готова"


@pytest.mark.asyncio
async def test_select_user_to_user_got_movies():
    request = MockedBot(MessageHandler(select_user_to_user))
    calls = await request.query(
        message=MESSAGE.as_object(text="Похожие пользователи"),
        user_data={
            12345678: {"user_to_user": {"content_type": "Фильм", "genre": "Ужасы"}}
        },
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message.startswith("Данные о вас уже есть:")


@pytest.mark.asyncio
async def test_reset_content_type_recommend():
    request = MockedBot(MessageHandler(reset_content_type))
    calls = await request.query(
        message=MESSAGE.as_object(text="Старт"), user_data={12345678: {}}
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Подборка готова"


@pytest.mark.asyncio
async def test_reset_content_type_change():
    request = MockedBot(MessageHandler(reset_content_type, state=UserToUserGroup.start))
    calls = await request.query(
        message=MESSAGE.as_object(text="изменить"), user_data={12345678: {}}
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Какой контент интересует?"
