import pytest
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from handlers.user_info import User, age, finish_user_data, income, kids, sex


@pytest.mark.asyncio
async def test_age():
    request = MockedBot(MessageHandler(age, state=User.age))
    calls = await request.query(message=MESSAGE.as_object(text="Да"))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Укажите возраст"


@pytest.mark.asyncio
async def test_income():
    request = MockedBot(MessageHandler(income, state=User.income))
    calls = await request.query(message=MESSAGE.as_object(text="35-44"))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Укажите доход"


@pytest.mark.asyncio
async def test_sex():
    request = MockedBot(MessageHandler(sex, state=User.sex))
    calls = await request.query(message=MESSAGE.as_object(text="20-40к"))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Укажите пол"


@pytest.mark.asyncio
async def test_kids():
    request = MockedBot(MessageHandler(kids, state=User.kids))
    calls = await request.query(message=MESSAGE.as_object(text="Женщина"))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Есть ли у вас дети?"


@pytest.mark.asyncio
async def test_finish():
    request = MockedBot(MessageHandler(finish_user_data, state=User.user_filled))
    calls = await request.query(message=MESSAGE.as_object(text="Да"))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Спасибо, теперь можно перейти к фильмам"
