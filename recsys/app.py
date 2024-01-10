from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models.item_to_item.infer import get_similar_items_inference_api
from models.personal.predict import get_movies_for_user


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
