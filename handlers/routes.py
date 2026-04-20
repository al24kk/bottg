from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite

router = Router()


# -------

DB_NAME = "al24k.sql"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
			CREATE TABLE IF NOT EXISTS users(
						id INTEGER PRIMARY KEY,
						full_name TEXT,
						age INTEGER
			)
                         """
        )
        await db.commit()


async def add_user(full_name, age):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO users (full_name, age) VALUES(?, ?)", (full_name, age)
        )
        await db.commit()


async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT full_name, age FROM users")
        result = await cursor.fetchall()
        return result


# -------


@router.message(Command("start"))
async def start(message: Message):
    await init_db()
    await message.answer("Hello!\nType /reg AGE")


@router.message(Command("reg"))
async def reg(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Enter the command right")
        return

    await add_user(message.from_user.full_name, int(parts[1]))

    await message.answer("Registration is done!")


@router.message(Command("users"))
async def users(message: Message):
    users = await get_users()

    if not users:
        await message.answer("Users is not exist")
        return

    text = "User in base:\n\n"
    for full_name, age in users:
        text += f"- {full_name} - <code>{age}</code>\n"
    await message.answer(text, parse_mode="HTML")
