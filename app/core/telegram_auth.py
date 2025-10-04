import hmac
import hashlib
import json
from typing import Optional
from urllib.parse import parse_qsl
from app.core.settings import settings


def get_telegram_user(init_data: str) -> Optional[dict]:
    """Получает и проверяет данные пользователя от Telegram"""
    try:
        if not init_data:
            return None

        # Парсим данные
        parsed_data = dict(parse_qsl(init_data))

        # Получаем hash
        received_hash = parsed_data.pop('hash', None)
        if not received_hash:
            return None

        # Создаем строку для проверки
        data_check_string = '\n'.join([
            f'{k}={v}' for k, v in sorted(parsed_data.items())
        ])

        # Создаем секретный ключ
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=settings.TELEGRAM_BOT_TOKEN.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Вычисляем hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Сравниваем хеши
        if calculated_hash != received_hash:
            return None

        # Парсим данные пользователя
        user_data = json.loads(parsed_data.get('user', '{}'))

        return user_data

    except Exception:
        return None