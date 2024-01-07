from fastapi import FastAPI
from fastapi.responses import JSONResponse
from infer import get_movies


app = FastAPI()


@app.get("/popular")
async def popular():
    resp = get_movies()
    return JSONResponse(content={"movies": resp})
