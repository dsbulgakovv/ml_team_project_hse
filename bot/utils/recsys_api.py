from aiohttp import ClientSession


class RecsysAPI:
    def __init__(self):
        self.base_url = "http://recsys-service:8000"

    async def get_personal(self, user_id):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/popular", params={"id": user_id}
            ) as resp:
                response = await resp.json()
        return response

    async def get_user_to_user(self, content_type, genre):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/user_to_user",
                params={"content_type": content_type, "genre": genre},
            ) as resp:
                response = await resp.json()
        return response

    async def get_movie_to_movie(self):
        async with ClientSession() as session:
            async with session.get(f"{self.base_url}/movie_to_movie") as resp:
                response = await resp.json()
        return response

    async def get_user_recommendation(self):
        async with ClientSession() as session:
            async with session.get(f"{self.base_url}/user_recommendation") as resp:
                response = await resp.json()
        return response
