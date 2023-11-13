from openai import AsyncOpenAI
from config import open_ai_api_key

client = AsyncOpenAI(api_key=open_ai_api_key)


# ответ гпт
async def gpt_response_creation(context):
    response = await client.chat.completions.create(  # создание ответа
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
