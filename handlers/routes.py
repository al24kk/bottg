from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite
import asyncio
from aiogram import Bot

router = Router()


subscribers = set()


async def notifier(bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "don't worry it's just a spam")
                except Exception:
                    pass

        await asyncio.sleep(10)


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Hello!\n"
        "I can help you with mailing!\n\n"
        "Commands: \n"
        "/subscribe - subscribe for mailing\n"
        "/unsubscribe - unsubscribe from mailing\n"
        "/subscribers - list of subscribers\n"
    )


@router.message(Command("subscribe"))
async def sub(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)

    await message.answer("You subscribed")


@router.message(Command("unsubscribe"))
async def unsub(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)

    await message.answer("You unsubscribed")


@router.message(Command("subscribers"))
async def subs(message: Message):
    if not subscribers:
        await message.answer("")
        return

    text = "Subscribers: \n"
    for uid in subscribers:
        text += f"{uid}\n"
    await message.answer(text)
