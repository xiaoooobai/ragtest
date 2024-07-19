from typing import Optional, Union, Iterable
from decorator import contextmanager
from core.db.base import DbConnector
from core.config.config import Config
import pymysql
config = Config()


class MySqlConnector(DbConnector):
    def __init__(self, auto_commit: bool = False,
                 database: Optional[str] = None,
                 cursor_type: pymysql.cursors.Cursor = pymysql.cursors.DictCursor,
                 *args, **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.host: str = self.host or config.get('MYSQL_DB_HOST') or 'localhost'
        self.port: int = self.port or int(config.get('MYSQL_DB_PORT')) or 3306
        self.user: str = self.user or config.get('MYSQL_DB_USER') or 'root'
        self.password: str = self.password or config.get('MYSQL_DB_PASSWORD') or '123456'
        self.database: str = database or config.get('MYSQL_DB_DATABASE') or 'test'
        self.auto_commit: bool = auto_commit
        self._cursor_type = cursor_type
        self._conn: Optional[pymysql.connections.Connection] = None

    def __del__(self):
        self.disconnect()

    def connect(self) -> bool:
        if self._conn is None:
            try:
                self._conn = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            except Exception as e:
                return False
        return True

    def reconnect(self) -> bool:
        self.disconnect()
        result = self.connect()
        return result

    @property
    def connection(self) -> pymysql.connections.Connection:
        return self._conn

    def disconnect(self):
        if self._conn is not None and self._conn.open:
            self._conn.close()

    def execute_sql(self,
                    sql: str,
                    params: Optional[Union[dict, Iterable]] = None,
                    fetch: bool = False,
                    fetch_all: bool = False):
        """
        执行 sql 语句
        :param sql:
        :param params: 参数
        :param fetch: 是否接受返回的数据
        :param fetch_all: 返回一条数据或全体数据。如果为 True，则返回所有数据；否则，仅返回一条数据。
        :return:
        """
        with self.connection.cursor(self._cursor_type) as cursor:
            cursor.execute(sql, params)
            if fetch:
                if fetch_all:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()
            if self.auto_commit:
                self.connection.commit()

    def commit(self):
        self._conn.commit()

    @contextmanager
    def auto_commit(self):
        original_auto_commit = self.auto_commit
        self.auto_commit = True
        try:
            yield self
        finally:
            self.auto_commit = original_auto_commit

