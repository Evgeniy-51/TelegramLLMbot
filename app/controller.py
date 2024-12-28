import requests
import logging

LLM_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
dialog_history: dict[int, list[dict]] = {}


async def reset_context(user_id) -> None:
    dialog_history[user_id] = []


async def get_qwen_response(user_id: int, user_message: str) -> str:
    messages = dialog_history.get(user_id, [])

    # Добавляем текущее сообщение пользователя
    messages.append({"role": "user", "content": user_message})

    try:
        # Отправляем запрос к локальной модели
        response = requests.post(
            LLM_API_URL,
            json={
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
            }
        )

        response.raise_for_status()
        assistant_message = response.json()['choices'][0]['message']['content']

        dialog_history[user_id].append({"role": "user", "content": user_message})
        dialog_history[user_id].append({"role": "assistant", "content": assistant_message})

        # Ограничиваем историю последними 10 сообщениями
        dialog_history[user_id] = dialog_history[user_id][-10:]

        return assistant_message

    except Exception as e:
        logging.error(f"Error getting LLM response: {e}")
        return f"Произошла ошибка при обращении к модели"
