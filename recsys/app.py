from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models.item_to_item.infer import get_similar_items_inference_api
from models.personal.predict import get_movies_for_user
from models.user_to_user.infer import pipline_user_to_user


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Movie recommender API based on KION data."}


@app.get("/popular")
async def popular(user_id: int):
    resp = get_movies_for_user(user_id)
    return JSONResponse(content={"movies": resp})


@app.get("/movie_to_movie/{movie_id}")
async def item_to_item(movie_id: int):
    resp = get_similar_items_inference_api(target_item=movie_id, k_recommended=10)
    return JSONResponse(content={"movies": resp})


@app.get("/user_to_user/{user_id}_{genre}_{content_type}")  # todo такой формат?
async def user_to_user(user_id: int, content_type: str, genre: str):
    """Функция получает на вход данные о пользователе и предпочтениях, возвращает dict в переменную resp_dict"""

    resp_dict = pipline_user_to_user(
        user_id=user_id, genre_input=genre, content_type_input=content_type
    )  # todo функция возвращает dict

    return JSONResponse(content=resp_dict)  # todo такой формат?
