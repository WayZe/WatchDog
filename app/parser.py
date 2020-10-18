import json
import time
import pickle
import logging
import requests
from requests import Response
from redis_storage import RedisStorage
from typing import Dict, Union, Optional
from functions import get_int_env, get_str_env


class Rater:
    """Класс для работы с курсами валют."""
    def __init__(self):
        self._currencies_to_emojis = {'USD': ':dollar:', 'EUR': ':euro:'}
        self._currencies_data: Optional[Dict[str, Dict[str, Union[str, float]]]] = None
        self._last_call: float = 0
        self._redis_storage = RedisStorage()

    @property
    def currencies_data(self) -> Dict[str, Dict[str, Union[str, float]]]:
        """Получаем курсы всех валют[USD, EUR].

        Returns:
            Dict[str, Dict[str, Union[str, float]]]: словарь {название_валюты: {'rate': курс, 'emoji': код_эмодзи}}
        """
        KEY: str = 'currency_data'
        currency_data_pickle: Optional[bytes] = self._redis_storage.get_dict(KEY)
        if currency_data_pickle is None:
            response: Response = self._get_response()
            currencies_data: Dict[str, Dict[str, Union[str, float]]] = self._get_currencies_data(response)
            self._redis_storage.save_dict(KEY, pickle.dumps(currencies_data), 3600)
        else:
            currencies_data = pickle.loads(currency_data_pickle)
            logging.warning(f'Получили словарь {KEY} из Redis')
        return currencies_data

    def _get_response(self) -> Response:
        """Получаем ответ от API с курсами валют."""
        url: str = ''
        url_code: int = get_int_env('URL_CODE')
        if url_code == 0:
            url = get_str_env('MAIN_URL')
            response = requests.get(url)
        elif url_code == 1:
            url = get_str_env('TEST_URL')
            response = requests.get(url, params={'base': 'USD'})
        else:
            logging.error(f'Введен некорректный URL_CODE {url_code}')
        logging.warning(f'Получили курсы валют c {url}')
        return response

    def _get_currencies_data(self, response: Response) -> Dict[str, Dict[str, Union[str, float]]]:
        """Получаем словарь с курсами валют из response.

        Args:
            response (Response): Ответ Api с курсами валют

        Returns:
            Dict[str, Dict[str, Union[str, float]]]: словарь с курсами валют вида
                                                     {название_валюты: {'rate': курс, 'emoji': код_эмодзи}}
        """
        RATE_LENGTH: int = 10000
        currencies_data = {}
        rates: Dict[str, float] = json.loads(response.text)['rates']
        for currency, emoji in self._currencies_to_emojis.items():
            # делаем базовой валютой RUB и обрезаем до четырех знаков после запятой
            rub_base_rate: float = int(rates['RUB'] / rates[currency] * RATE_LENGTH) / RATE_LENGTH
            currencies_data.update({
                currency: {
                    'rate': rub_base_rate,
                    'emoji': emoji
                }
            })
        return currencies_data
