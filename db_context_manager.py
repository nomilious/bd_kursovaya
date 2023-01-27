from typing import Optional
from pymysql import connect
from pymysql.cursors import Cursor
from pymysql.connections import Connection
from pymysql.err import OperationalError


class DBContextManager:
    """Класс для подключения к БД и выполнения sql-запросов."""
    def __init__(self, config: dict):
        self.config: dict = config
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    def __enter__(self) -> Optional[Cursor]:
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Invalid login or password')
            elif err.args[0] == 1049:
                print('Check database name')
            else:
                print(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tr) -> bool:
        if exc_type:
            print(f"Error type: {exc_type.__name__}")
            print(f"DB error: {' '.join(exc_val.args)}")

        if self.conn and self.cursor:
            if exc_val:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True