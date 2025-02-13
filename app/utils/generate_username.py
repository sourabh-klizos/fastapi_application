import random
import string

from app.database.db import get_db
from fastapi import Depends


async def generate_random_string(length: int = 2) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


async def generate_available_username(username: str, db) -> list[str]:

    user_collection = db["users"]
    available_usernames = list()
    while True:
        generated_username = username + await generate_random_string()
        generated_username_exists = await user_collection.find_one(
            {"username": generated_username}
        )
        if generated_username_exists:
            continue

        available_usernames.append(generated_username)
        if len(available_usernames) == 5:
            break

    return available_usernames
