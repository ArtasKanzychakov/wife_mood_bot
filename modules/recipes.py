# modules/recipes.py

import aiohttp
import random

SPOONACULAR_API_KEY = "YOUR_SPOONACULAR_API_KEY"

async def get_recipe_carousel():
    query = random.choice(["summer salad", "light soup", "berry dessert"])
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&number=5&apiKey={SPOONACULAR_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    recipes = []
    for item in data.get("results", []):
        recipes.append({
            "type": "photo",
            "media": item["image"],
            "caption": f"🍲 {item['title']}"
        })

    return recipes
