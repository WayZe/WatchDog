import logging
from psycopg2 import sql, connect
from functions import get_str_env


class PostgresStorage:
    def __init__(self):
        postgres_url = get_str_env('DATABASE_URL')
        self._connection = connect(postgres_url)
        logging.warning(f'Postgres {postgres_url} инициализирован.')

    def add_user(self, user_id: int):
        cursor = self._connection.cursor()
        cursor.execute(
            'INSERT INTO users (id) VALUES (%s) ON CONFLICT DO NOTHING',
            (user_id,)
        )
        self._connection.commit()
