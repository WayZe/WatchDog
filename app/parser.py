import json
import requests
from typing import Dict, Union
from functions import get_int_env, get_str_env


class Rater:
    def __init__(self):
        self.currencies_to_emojis = {'USD': ':dollar:', 'EUR': ':euro:'}

    # Получаем курсы всех валют
    def get_all(self) -> Dict[str, Dict[str, Union[str, float]]]:
        currencies_data: Dict[str, Dict[str, Union[str, float]]] = {}
        url: str = get_str_env('URL')
        for currency, emoji in self.currencies_to_emojis.items():
            response = requests.get(url, params={'base': currency})
            rate: float = json.loads(response.text)['rates']['RUB']
            currencies_data.update({currency: {'rate': rate, 'emoji': emoji}})
        return currencies_data
