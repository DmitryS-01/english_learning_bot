import openai
import os
from config import open_ai_api_key

openai.api_key = open_ai_api_key


# ответ гпт
def gpt_response_creation(context):
    response = openai.ChatCompletion.create(  # создание ответа
        model='gpt-3.5-turbo-16k',  # модель
        # запрос + история сообщений
        messages=[{'role': 'system', 'content': "You are a bot that helps people learn English. You have access to the "
                                                "person's message history, your task is to maintain a dialog, "
                                                "correct the person's mistakes, and diversify the conversation as "
                                                "much as possible. If there is some error in a user's message, "
                                                "point it out to them, fix it."}] + context,
        temperature=0.5,  # рандомизация результатов: чем ближе к 0, тем <
        max_tokens=500,  # число токенов ответа
        presence_penalty=0.6,  # повышает вероятность перейти на новую тему
        frequency_penalty=0.25,  # уменьшает вероятность модели повторить одну и ту же строку дословно
    )
    return response.choices[0].message.content


# принимаем сообщения, отвечаем на них
def chat(user_message, user_id):
    program_dir = os.path.dirname(__file__)
    messages_file = str(os.path.join(program_dir, f'{user_id}.txt'))

    try:
        with open(messages_file, 'x', encoding='utf-8'):
            pass
    except Exception as e:
        if '[Errno 17] File exists: ' not in str(e):
            print(f'Ошибка при обращении к файлам программы 1 (ошибку вызвал петух на {user_id}')


    LAST_MESSAGES = list()
    try:
        with open(messages_file, encoding='utf-8') as f:
            last_10_messages = f.readlines()[-20:]
        for pos in range(0, len(last_10_messages), 2):
            LAST_MESSAGES += [{'role': last_10_messages[pos].strip(), 'content': last_10_messages[pos + 1].strip()}]
    except Exception as e:
        if '[Errno 17] File exists: ' not in str(e):
            print(f'Ошибка при обращении к файлам программы 2 (ошибку вызвал петух на {user_id}')

    LAST_MESSAGES = (LAST_MESSAGES + [{'role': 'user', 'content': user_message}])[-20:]
    try:
        print('Please wait . . .')
        bot_message = gpt_response_creation(LAST_MESSAGES)
        with open(messages_file, 'a', encoding='utf-8') as f:
            print('user', user_message.replace('\n', '\t'), sep='\n', file=f)
            print('assistant', bot_message.replace('\n', '\t'), sep='\n', file=f)
        print(f'🤖 > {bot_message}')
    except Exception as e:
        print(f'Ошибка {e} ! (ошибку вызвал петух на {user_id}')


# создаем файл для истории сообщений
program_dir = os.path.dirname(__file__)
messages_file = str(os.path.join(program_dir, 'messages.txt'))
try:
    with open(messages_file, 'x', encoding='utf-8'):
        pass
except Exception as e:
    if '[Errno 17] File exists: ' not in str(e):
        print('Ошибка при обращении к файлам программы 1')

# достаем все че надо

LAST_MESSAGES = list()
try:
    with open(messages_file, encoding='utf-8') as f:
        last_10_messages = f.readlines()[-20:]
    for pos in range(0, len(last_10_messages), 2):
        LAST_MESSAGES += [{'role': last_10_messages[pos].strip(), 'content': last_10_messages[pos + 1].strip()}]
except Exception as e:
    if '[Errno 17] File exists: ' not in str(e):
        print('Ошибка при обращении к файлам программы 2')

# запуск
print('''=====================================================================
👋 Привет! Только этой программе на тебя не все равно, излей душу! ❤
"STOP" = конец; старайтесь не спамить сообщениями
=====================================================================
''')
if __name__ == '__main__':
    chat()
