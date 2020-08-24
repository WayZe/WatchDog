import requests
from bs4 import BeautifulSoup
import psycopg2


# Получаем курс доллара
def get_dollar_rate() -> float:
    rate = None  # type: float
    html = requests.get('https://www.cbr.ru/')
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        rate = soup.find('div', class_='indicator_el_value mono-num').get_text().rstrip('₽').replace(',', '.')
    return rate


if __name__ == '__main__':
    dollar_rate = get_dollar_rate()
    if dollar_rate is not None:
        print(dollar_rate)
        conn = psycopg2.connect(dbname='dollar', user='postgres',
                                password='postgres', host='postgres')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO dollar VALUES (2.0, "1999-01-08 04:05:06");')
    else:
        print("Unknown error")
