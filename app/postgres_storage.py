import logging
from typing import List
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
        cursor.close()

    def get_user_ids_to_notify(self) -> List[int]:
        cursor = self._connection.cursor()
        cursor.execute('SELECT id FROM users WHERE notify = TRUE')
        user_ids: List[int] = [i[0] for i in cursor.fetchall()]
        cursor.close()
        return user_ids

    def get_notification_state_for_user(self, user_id: int) -> bool:
        cursor = self._connection.cursor()
        cursor.execute('SELECT notify FROM users WHERE id = %s', (user_id,))
        state: bool = cursor.fetchone()[0]
        cursor.close()
        return state

    def set_notification_for_user(self, user_id: int, state: bool):
        cursor = self._connection.cursor()
        cursor.execute(
            'UPDATE users SET notify = %s WHERE id = %s',
            (state, user_id)
        )
        self._connection.commit()
        cursor.close()
