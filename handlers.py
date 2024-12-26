from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from controller import get_llm_response

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я бот, который может общаться с помощью LLM модели. Отправьте мне ваш вопрос.")


@router.message(F.text)
async def llm_request(message: Message):
    llm_response = await get_llm_response(message.text)
    await message.answer(llm_response)


@router.message()
async def message_handler(message: Message):
    await message.answer("Я понимаю только текстовые запросы")
