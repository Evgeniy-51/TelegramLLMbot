from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.controller import get_qwen_response, reset_context

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await reset_context(message.from_user.id)
    await message.answer("Привет! Я бот, который может общаться с помощью LLM модели. Отправьте мне ваш вопрос.")


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    HELP_TEXT = """
    Этот бот позволяет общаться с нейросетью, поддерживая контекст беседы.
    Если хотите начать новый чат - выберите пункт меню 'New Chat'
    """
    await message.answer(text=HELP_TEXT)


@router.message(F.text)
async def llm_request(message: Message):
    user_id = message.from_user.id
    user_message = message.text

    # Получаем ответ от модели
    response = await get_qwen_response(user_id, user_message)

    # Отправляем ответ пользователю
    await message.answer(response)


@router.message()
async def message_handler(message: Message):
    await message.answer("Я понимаю только текстовые запросы")
