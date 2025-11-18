from ..database.DAO import dao, DAO

from abc import ABC


class Service(ABC):
    def __init__(self):
        self._dao: DAO = dao
        pass
