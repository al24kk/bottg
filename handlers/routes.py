from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router = Router()

import aiohttp
import ssl
import certifi

# ------------------------------------------------------


async def get_product(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            print("STATUS:", resp.status)

            if resp.status == 404:
                return None

            data = await resp.json()
            return data


# ------------------------------------------------------


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Hello! I'm just an online shop bot.\nType command /product ID\n\nПример: <b>/product 1</b>",
        parse_mode="HTML",
    )


@router.message(Command("product"))
async def get_product_cmd(message: Message):
    parts = message.text.strip().split()

    # /product 2 some [EXAMPLE]

    if len(parts) < 2:
        await message.answer("Use: /product 1")
        return

    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer("Product ID has to be a digit")
        return

    await message.answer(f"Find product with {product_id}...")

    try:
        product = await get_product(int(product_id))
    except Exception as e:
        await message.answer(f"ERROR: {e}")
        return

    if product is None:
        await message.answer("No such product")
        return

    title = product.get("title", "Untitled")
    price = product.get("price", "--")
    desc = product.get("description", "without description")
    category = product.get("category", "without category")
    image = product.get("image")

    text = (
        f"<b>{title}</b>\n\n"
        f"Category: <i>{category}</i>\n"
        f"Price: <b>{price}$</b>\n"
        f"{desc}"
    )

    photo = FSInputFile("sad ye.png")
    await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")

    # if image:
    #     await message.answer_photo(photo=image, caption=text, parse_mode="HTML")
    # else:
    #     await message.answer(text, parse_mode="HTML")
