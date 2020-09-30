import time
import requests
from typing import Optional
from bs4 import BeautifulSoup


TIMEOUT = 60


# Получаем курс доллара
def get_dollar_rate() -> Optional[float]:
    rate: Optional[float] = None
    html = requests.get('https://www.cbr.ru/')
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        rate = soup.find('div', class_='indicator_el_value mono-num').get_text().rstrip('₽').replace(',', '.')
    return rate


if __name__ == '__main__':
    while True:
        dollar_rate = get_dollar_rate()
        if dollar_rate is not None:
            print(dollar_rate)
        else:
            print("Unknown error")
        time.sleep(TIMEOUT)
