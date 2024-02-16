import pytest
from aiogram.filters import Command
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from app import command_start_handler


@pytest.mark.asyncio
async def test_start():
    request = MockedBot(
        MessageHandler(command_start_handler, Command(commands=["start"]))
    )
    calls = await request.query(message=MESSAGE.as_object(text="/start"), user_data={})

    answer_message = calls.send_message.fetchall()
    assert answer_message[0].text == "Привет, <b>FirstName LastName</b>!"
    assert answer_message[1].text == "Посоветовать фильм?"
