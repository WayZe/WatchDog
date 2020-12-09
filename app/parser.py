import json
import time
import emojis
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
        self._last_call: float = 0
        self._KEY: str = 'currency_data'
        self._redis_storage = RedisStorage()
        self._TEMP_KEY: str = f'temp_{self._KEY}'
        self._PREV_KEY: str = f'prev_{self._KEY}'
        self._currencies_to_emojis = {'USD': ':dollar:', 'EUR': ':euro:'}
        self._currencies_data: Optional[Dict[str, Dict[str, Union[str, float]]]] = None
        self._diffs_to_emojis = {
            'up': ':arrow_up:',
            'down': ':arrow_down:'
        }

    def formatted_currencies(self):
        formatted_currencies: str = ''
        for currency, value in self.currencies_data.items():
            diff: str = self._diffs_to_emojis['up'] if value['diff'] > 0 else self._diffs_to_emojis['down']
            formatted_currencies = formatted_currencies + emojis.encode(
                f"{value['emoji']} Курс {currency} {value['rate']} {diff}\n"
            )
        return formatted_currencies

    @property
    def currencies_data(self) -> Dict[str, Dict[str, Union[str, float]]]:
        """Получаем курсы всех валют[USD, EUR].

        Returns:
            Dict[str, Dict[str, Union[str, float]]]: словарь {название_валюты: {'rate': курс, 'emoji': код_эмодзи}}
        """
        currency_data_pickle: Optional[bytes] = self._redis_storage.get_dict(self._KEY)
        if currency_data_pickle is None:
            self._redis_storage.move_value(self._TEMP_KEY, self._PREV_KEY)
            response: Response = self._get_response()
            currencies_data: Dict[str, Dict[str, Union[str, float]]] = self._get_currencies_data(response)
            pickled_currency_data: bytes = pickle.dumps(currencies_data)
            self._redis_storage.save_dict(self._KEY, pickled_currency_data, 600)
            self._redis_storage.save_dict(self._TEMP_KEY, pickled_currency_data)
        else:
            currencies_data = pickle.loads(currency_data_pickle)
            logging.warning(f'Получили словарь {self._KEY} из Redis')

        if self._redis_storage.get_dict(self._PREV_KEY):
            currencies_data = self._calculate_difference(currencies_data)

        return currencies_data

    def _calculate_difference(
        self,
        currencies_data: Dict[str, Dict[str, Union[str, float]]]
    ) -> Dict[str, Dict[str, Union[str, float]]]:
        """Рассчитываем разницу между предыдущим курсами и текущими."""
        prev_currencies_data: Dict[str, Dict[str, Union[str, float]]] = pickle.loads(
            self._redis_storage.get_dict(self._PREV_KEY)
        )
        for currency, value in currencies_data.items():
            currencies_data[currency]['diff'] = value['rate'] - prev_currencies_data[currency]['rate']
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
        fake_api: int = get_int_env('FAKE_API')
        if fake_api == 1:
            f = open('fake_api.json', 'r')
            rates: Dict[str, float] = json.loads(f.read())['rates']
            f.close()
        else:
            rates = json.loads(response.text)['rates']

        logging.warning(rates)
        for currency, emoji in self._currencies_to_emojis.items():
            # делаем базовой валютой RUB и обрезаем до четырех знаков после запятой
            rub_base_rate: float = int(rates['RUB'] / rates[currency] * RATE_LENGTH) / RATE_LENGTH
            currencies_data.update({
                currency: {
                    'rate': rub_base_rate,
                    'emoji': emoji,
                    'diff': .0
                }
            })
        return currencies_data
