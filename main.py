import asyncio
import logging
import sys
import os
from datetime import datetime, timedelta

from config import bot_token, delta_time  # delta_time - задержка между некст обращением к OpenAI
from message_processing import gpt_response_creation


from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold



dp = Dispatcher()

# очередь на отправку запроса в OpenAI
queue = tuple()
# номер сообщения
num = 1

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\nЯ научу тебя базарить с пиндосами")


@dp.message()
async def lame_message_handler(message: types.Message) -> None:

    global num, queue, last_use_time

    # id пользователя и текст его сообщения
    user_message = message.text
    user_id = message.chat.id

    try:
        # расположение файла с иторией общения с данным персонажем
        messages_file = str(os.path.join(dialogues_folder, f'{user_id}.txt'))

        # если этого файла нет, создаем его
        try:
            with open(messages_file, 'x', encoding='utf-8'):
                pass
        except Exception as e:
            if '[Errno 17] File exists: ' not in str(e):
                print(f'Ошибка при обращении к файлам программы 1 (ошибку вызвал петух на {user_id})')

        # достаем 10 последних сообщений
        last_messages = list()
        try:
            with open(messages_file, encoding='utf-8') as f:
                last_10_messages = f.readlines()[-20:]
            for pos in range(0, len(last_10_messages), 2):
                last_messages += [{'role': last_10_messages[pos].strip(), 'content': last_10_messages[pos + 1].strip()}]
        except Exception as e:
            if '[Errno 17] File exists: ' not in str(e):
                print(f'Ошибка при обращении к файлам программы 2 (ошибку вызвал петух на {user_id})')
        # добавляем к ним текущее сообщение этого петушары
        last_messages = (last_messages + [{'role': 'user', 'content': user_message}])[-20:]

        # встали в очередь
        pos, num = num, num + 1
        queue += (pos,)
        try:
            await message.answer('Please wait . . .')

            # ожидание очереди
            while queue.index(pos) != 0 or last_use_time + timedelta(seconds=delta_time) > datetime.utcnow():
                await asyncio.sleep(1)
            # получаем ответ от модели
            bot_answer = await gpt_response_creation(last_messages)

            # дописываем историю
            with open(messages_file, 'a', encoding='utf-8') as f:
                print('user', user_message.replace('\n', '\t'), sep='\n', file=f)
                print('assistant', bot_answer.replace('\n', '\t'), sep='\n', file=f)

            # отвечаем этому пидрилле
            await message.reply(f'🤖 > {bot_answer}')

            # прорабатываем упущения
        except Exception as e:
            print(f'Ошибка {e} ! (ошибку вызвал петух на {user_id}')
        finally:
            # двигаем очередь
            queue, last_use_time = queue[1:], datetime.utcnow()
    except Exception as e:
        print(f"тварь на {message.from_user.id} / {message.from_user.full_name} че то сломала")


async def main() -> None:
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # создаем папку для диалогов
    if not os.path.isdir("dialogues"):
        os.mkdir("dialogues")
    program_dir = os.path.dirname(__file__)
    dialogues_folder = os.path.join(program_dir, "dialogues")

    # запоминаем время запуска проги, чтоб просчитывать, когда можно будет отправить запрос
    last_use_time = datetime.utcnow()

    asyncio.run(main())
