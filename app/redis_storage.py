import redis
import logging
from typing import Dict, Optional
from functions import get_str_env, get_int_env


class RedisStorage:
    """Класс для работы с Redis."""
    def __init__(self):
        redis_url: str = get_str_env('REDIS_URL')
        is_production: int = get_int_env('IS_PRODUCTION')
        if is_production == 1:
            self._connection = redis.from_url(redis_url)
        elif is_production == 0:
            self._connection = redis.Redis(host=redis_url)
        else:
            raise(f'Задана неизвестная версия конфигурации сервиса {is_production}')
        logging.warning(f"Redis {redis_url} инициализирован.")

    def save_dict(self, redis_key: str, redis_dict: str, ttl: Optional[int] = None):
        """Записываем словарь в Redis."""
        self._connection.set(redis_key, redis_dict)
        if ttl is not None:
            self._connection.expire(redis_key, ttl)

    def get_dict(self, redis_key: str) -> Dict:
        """Получаем словарь из Redis."""
        return self._connection.get(redis_key)

    def move_value(self, from_key: str, to_key: str):
        """Передвигакм значение из ключа from_key в ключ to_key,
        если from_key пустой, то ничего не делаем.
        """
        from_value: str = self._connection.get(from_key)
        if from_value is not None:
            self.save_dict(to_key, from_value)
