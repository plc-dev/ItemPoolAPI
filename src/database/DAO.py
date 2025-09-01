from typing import Dict
from ..models.Task import TaskMaterial, Task

class DAO:
    """
    TODO: Integrate a proper database

    This is merely a mock-DB-class, which per design doesn't persist anything permanently.
    It can potentially be instantiated many times without sharing state. 
    Emulating the behaviour of a database with a shared state could be achieved by implementing it with the Singleton or Borg/Monostate pattern.
    """
    def __init__(self):
        self._materials_db: Dict[int, TaskMaterial] = {}
        self._tasks_db: Dict[int, Task] = []
        self._material_id_counter = 0
        self._task_id_counter = 0

    def store_task_material(self, material: TaskMaterial) -> int | None:
        self._material_id_counter = self._material_id_counter + 1
        self._materials_db[self._material_id_counter] = material

        return self._material_id_counter
    
    def store_task(self, task: Dict) -> int | None:
        self._material_id_counter = self._material_id_counter + 1

        self._tasks_db[self._material_id_counter] = {
            "stimulus_ids": task["stimulus_ids"],
            "solution_ids":task["solution_ids"]
        }

        return self._material_id_counter
    
    def get_task_material(self, id: int) -> int | None:
        if id in self._materials_db:
            return self._materials_db[id]
        return None
    
dao = DAO()