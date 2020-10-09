import os
from typing import Optional


# получаем переменную окружения строкового типа
def get_str_env(name: str):
    value: Optional[str] = os.getenv(name)
    if value is None:
        raise Exception(f'Не удалось получить переменную окружения {name}')
    return str(value)


# получаем переменную окружения целочисленного типа
def get_int_env(name: str):
    return int(get_str_env(name))
