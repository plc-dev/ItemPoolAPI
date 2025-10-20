from ..database.DAO import dao, DAO

from abc import ABC

class Controller(ABC):
    def __init__(self):
        self._dao: DAO = dao
        pass