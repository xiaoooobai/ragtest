from abc import ABC, abstractmethod
from typing import Optional


class DbConnector(ABC):
    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,):
        self.host: Optional[str] = host
        self.port: Optional[int] = port
        self.user: Optional[str] = user
        self.password: Optional[str] = password

    @abstractmethod
    def connect(self) -> bool:
        """
        :return: 返回是否正常开启连接
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError("not implemented")
