import time
import json
import requests
from dotenv import load_dotenv
from functions import get_int_env, get_str_env


# Получаем курс доллара
def get_usd_rate() -> float:
    url: str = get_str_env('URL')
    response = requests.get(url, params={'base': 'USD'})
    rate: float = json.loads(response.text)['rates']['RUB']
    return rate


if __name__ == '__main__':
    load_dotenv()

    while True:
        usd_rate = get_usd_rate()
        if usd_rate is not None:
            print(usd_rate)
        else:
            print('Не удалось получить курс usd.')
        timeout: int = get_int_env('TIMEOUT')
        time.sleep(timeout)
