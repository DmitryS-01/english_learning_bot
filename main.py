import asyncio
import logging
import sys


from config import bot_token


from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\nЯ научу тебя базарить с пиндосами")


@dp.message()
async def lame_message_handler(message: types.Message) -> None:
    try:
        bot_answer = 'TEST BROOOOOOOO'
        await message.answer(bot_answer)
    except Exception as e:
        print(f"тварь на {message.from_user.id} / {message.from_user.full_name} че то сломала")


async def main() -> None:
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
