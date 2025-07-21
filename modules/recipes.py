# modules/recipes.py

import aiohttp
import random
import os

API_KEY = os.getenv("SPOONACULAR_API_KEY")  # ключ из env

BASE_URL = "https://api.spoonacular.com/recipes/random?number=1"

async def get_recipe():
    params = {"apiKey": API_KEY, "tags": "seasonal,dinner"}
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            data = await resp.json()
            if "recipes" in data and data["recipes"]:
                recipe = data["recipes"][0]
                title = recipe["title"]
                instructions = recipe.get("instructions", "Инструкции отсутствуют.")
                return f"🍽 Блюдо дня: {title}\n\n{instructions}"
            else:
                return "Не удалось получить рецепт сегодня."
