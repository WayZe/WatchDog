import json
import requests
from functions import get_int_env, get_str_env


class Rater:
    # Получаем курс доллара
    @staticmethod
    def get_usd_rate() -> float:
        url: str = get_str_env('URL')
        response = requests.get(url, params={'base': 'USD'})
        rate: float = json.loads(response.text)['rates']['RUB']
        return rate
