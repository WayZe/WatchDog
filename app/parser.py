import json
import time
import logging
import requests
from typing import Dict, Union, Optional
from functions import get_int_env, get_str_env


class Rater:
    def __init__(self):
        self._currencies_to_emojis = {'USD': ':dollar:', 'EUR': ':euro:'}
        self._currencies_data: Optional[Dict[str, Dict[str, Union[str, float]]]] = None
        self._last_call: float = 0

    @property
    def currencies_data(self) -> Dict[str, Dict[str, Union[str, float]]]:
        """Получаем курсы всех валют[USD, EUR].

        Returns:
            Dict[str, Dict[str, Union[str, float]]]: словарь {название_валюты: {'rate': курс, 'emoji': код_эмодзи}}
        """
        new_call = time.time()
        # сбрасываем кэш, если прошло больше часа
        if (new_call - self._last_call) / 3600 > 1:
            self._last_call = new_call
            self._currencies_data = None

        if self._currencies_data is None:
            logging.warning(f'Получаем курсы валют c {get_str_env("URL")}')
            self._currencies_data = {}
            url: str = get_str_env('URL')
            for currency, emoji in self._currencies_to_emojis.items():
                response = requests.get(url, params={'base': currency})
                rate: float = json.loads(response.text)['rates']['RUB']
                self._currencies_data.update({currency: {'rate': rate, 'emoji': emoji}})
        return self._currencies_data
