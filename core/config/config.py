import os
from typing import Any, Dict
from core.base.clz import singleton
from dotenv import load_dotenv
import logging


@singleton
class Config:
    def __init__(self):
        load_dotenv()
        self.CONFIG: Dict[str, Any] = {
            'MYSQL_DB_HOST': os.environ.get('MYSQL_DB_HOST', '192.168.88.99'),
            'MYSQL_DB_PORT': os.environ.get('MYSQL_DB_PORT', '3306'),
            'MYSQL_DB_USER': os.environ.get('MYSQL_DB_USER', 'root'),
            'MYSQL_DB_PASSWORD': os.environ.get('MYSQL_DB_PASSWORD', 'not set'),
        }

        self.default_logger = self.get_logger()

        self._config = {
            k.lower(): v
            for k, v in self.CONFIG.items()
        }

    def get(self, key: str, ignore_case: bool = True) -> Any:
        """
        用来获取相关配置
        :param key: 需要找的键
        :param ignore_case: 是否忽略大小写
        :return: 如果存在，返回结果；如果不存在，返回 None
        """
        if ignore_case:
            return self._config.get(key.lower())
        else:
            return self._config.get(key)

    def get_logger(self, key: str = 'ragtest') -> logging.Logger:
        return logging.getLogger(key)