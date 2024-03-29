from aiohttp import ClientSession
from constraints.genres import content_type_mapping


class RecsysAPI:
    def __init__(self):
        self.base_url = "http://recsys-service:8000"

    async def get_personal(self, user_id):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/popular", params={"user_id": user_id}
            ) as resp:
                response = await resp.json()
        return response

    async def get_user_to_user(self, user_id, content_type, genre):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/user_to_user",
                params={
                    "user_id": user_id,
                    "content_type": content_type_mapping.get(content_type),
                    "genre": genre,
                },
            ) as resp:
                response = await resp.json()
        return response

    async def get_movie_to_movie(self, movie):
        async with ClientSession() as session:
            async with session.get(f"{self.base_url}/movie_to_movie/{movie}") as resp:
                response = await resp.json()
        return response
