import pytest
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from handlers.recommend import (
    Recommendation,
    UserToUserGroup,
    popular,
    reset_content_type,
    select_personal,
    select_user_to_user,
    set_content_type,
    set_genre,
    similar_movie,
    user_to_user,
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


@pytest.mark.asyncio
async def test_set_content_type():
    request = MockedBot(
        MessageHandler(set_content_type, state=UserToUserGroup.content_type)
    )
    calls = await request.query(
        message=MESSAGE.as_object(text="Фильм"), user_data={12345678: {}}
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Какой жанр показать?"


@pytest.mark.asyncio
async def test_set_genre():
    request = MockedBot(MessageHandler(set_genre, state=UserToUserGroup.genre))
    calls = await request.query(
        message=MESSAGE.as_object(text="Фильм"),
        user_data={12345678: {"user_to_user": {}}},
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Все готово"


@pytest.mark.asyncio
async def test_recommend_popular():
    request = MockedBot(MessageHandler(popular, state=Recommendation.popular))
    calls = await request.query(
        message=MESSAGE.as_object(text="Посоветуй фильм"), user_data={12345678: {}}
    )

    answer_message = calls.send_photo.fetchone()
    assert answer_message.caption.startswith("<b>Хрустальный")


@pytest.mark.asyncio
async def test_recommend_popular_stop():
    request = MockedBot(MessageHandler(popular, state=Recommendation.popular))
    calls = await request.query(
        message=MESSAGE.as_object(text="Хватит"), user_data={12345678: {}}
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Заканчиваю"


@pytest.mark.asyncio
async def test_recommend_popular_similar():
    request = MockedBot(MessageHandler(popular, state=Recommendation.popular))
    calls = await request.query(
        message=MESSAGE.as_object(text="Похожий на этот"), user_data={12345678: {}}
    )

    answer_message = calls.send_message.fetchall()
    assert answer_message[0].text == "Подбираю"
    assert answer_message[1].text == "Готово"


@pytest.mark.asyncio
async def test_recommend_user_to_user():
    request = MockedBot(MessageHandler(user_to_user, state=Recommendation.similar_users))
    calls = await request.query(
        message=MESSAGE.as_object(text="Посоветуй фильм"),
        user_data={
            12345678: {"user_to_user": {"genre": "ужасы", "content_type": "Фильмы"}}
        },
    )

    answer_message = calls.send_photo.fetchone()
    assert answer_message.caption.startswith("<b>Приворот")


@pytest.mark.asyncio
async def test_recommend_user_to_user_stop():
    request = MockedBot(MessageHandler(user_to_user, state=Recommendation.similar_users))
    calls = await request.query(
        message=MESSAGE.as_object(text="Хватит"),
        user_data={
            12345678: {"user_to_user": {"genre": "ужасы", "content_type": "Фильмы"}}
        },
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Заканчиваю"


@pytest.mark.asyncio
async def test_recommend_user_to_user_similar():
    request = MockedBot(MessageHandler(user_to_user, state=Recommendation.similar_users))
    calls = await request.query(
        message=MESSAGE.as_object(text="Похожий на этот"),
        user_data={
            12345678: {"user_to_user": {"genre": "ужасы", "content_type": "Фильмы"}}
        },
    )

    answer_message = calls.send_message.fetchall()
    assert answer_message[0].text == "Подбираю"
    assert answer_message[1].text == "Готово"


@pytest.mark.asyncio
async def test_recommend_movie_to_movie():
    request = MockedBot(
        MessageHandler(similar_movie, state=Recommendation.similar_movies)
    )
    calls = await request.query(
        message=MESSAGE.as_object(text="Посоветуй фильм"),
        user_data={12345678: {"last_movie": 10440}},
    )

    answer_message = calls.send_photo.fetchone()
    assert answer_message.caption.startswith("<b>Слепой")


@pytest.mark.asyncio
async def test_recommend_movie_to_movie_stop():
    request = MockedBot(
        MessageHandler(similar_movie, state=Recommendation.similar_movies)
    )
    calls = await request.query(
        message=MESSAGE.as_object(text="Хватит"),
        user_data={12345678: {"last_movie": 10440}},
    )

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Заканчиваю"


@pytest.mark.asyncio
async def test_recommend_movie_to_movie_similar():
    request = MockedBot(
        MessageHandler(similar_movie, state=Recommendation.similar_movies)
    )
    calls = await request.query(
        message=MESSAGE.as_object(text="Похожий на этот"),
        user_data={12345678: {"last_movie": 10440}},
    )

    answer_message = calls.send_message.fetchall()
    assert answer_message[0].text == "Подбираю"
    assert answer_message[1].text == "Готово"
