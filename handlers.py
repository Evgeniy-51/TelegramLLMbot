import requests
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

# LLM API endpoint
LLM_API_URL = "http://127.0.0.1:1234/v1/chat/completions"


async def get_llm_response(prompt: str) -> str:
    """
    Get response from local LLM model
    """
    try:
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": "meta-llama-3.1-8b-instruct",
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error getting LLM response: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."


@router.message(CommandStart())
async def start_handler(message: Message):
    """
    Handle /start command
    """
    await message.answer("Привет! Я бот, который может общаться с помощью LLM модели. Отправьте мне ваш вопрос.")


@router.message()
async def message_handler(message: Message):
    """
    Handle all other messages
    """
    user_message = message.text

    # Send "typing" action while processing
    await message.bot.send_chat_action(message.chat.id, "typing")

    # Get response from LLM
    llm_response = await get_llm_response(user_message)

    # Send response back to user
    await message.answer(llm_response)
