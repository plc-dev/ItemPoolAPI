
from ...models.Task import TaskType, MaterialType, TaskRegistrationRequestObject, TaskMaterialRegistrationRequestObject, ResponseStatus, TaskMaterial
from ..BaseController import Controller
from .TaskMaterialRegistrationHandlers.BaseHandler import TaskMaterialHandler
from .TaskRegistrationHandlers.BaseHandler import TaskHandler
from .TaskRegistrationHandlers.SQLTaskHandler import SQLTaskHandler

from .TaskMaterialRegistrationHandlers.MaterialHandlers import material_handlers

import logging

class TaskMaterialRegistrationController(Controller):
    """
    This class handles the registration of task-material with the system.
    The handling of new task-materials is supported by adding more material-handlers to the class.
    """
    def __init__(self):
        super().__init__()
        self._material_handlers: dict[str, TaskMaterialHandler] = {
            type: handler(self._dao) for type, handler in material_handlers.items()
        }

    def _select_material_handler(self, type: MaterialType):
        return self._material_handlers[type]

    def register_material(self, request: TaskMaterialRegistrationRequestObject):
        material_type = request.type
        material = request.material_information

        material_handler = self._material_handlers[material_type]
        metadata = material_handler.process_material(material)

        material.metadata = metadata

        id = self._dao.store_task_material(material)

        return id
    

class TaskRegistrationController(Controller):
    """
    This class handles the registration of tasks with the system.
    The handling of new tasks is supported by adding more task-handlers to the class.
    """
    def __init__(self):
        super().__init__()
        self._material_registration_controller = TaskMaterialRegistrationController()

        self._task_handlers: dict[str, TaskHandler] = {
            TaskType.sql: SQLTaskHandler(self._dao, self._material_registration_controller)
        }

    def _select_task_handler(self, type: TaskType):
        return self._task_handlers[type]

    def register_task(self, request: TaskRegistrationRequestObject):
        task_type = request.type

        task_handler = self._select_task_handler(task_type)
        processed_task = task_handler.process_task(request.task)

        if processed_task["result"] == ResponseStatus.error:
            return processed_task
        
        id = self._dao.store_task(processed_task)

        # Umbau: falls stimulus_ids/solution_ids Listen sind, wrappe sie in Dicts
        stimulus_ids = processed_task.get("stimulus_ids")
        solution_ids = processed_task.get("solution_ids")

        if isinstance(stimulus_ids, list):
            stimulus_ids = {"instruction": stimulus_ids}
        if isinstance(solution_ids, list):
            solution_ids = {"query": solution_ids}

        return {**processed_task, "id": id, "stimulus_ids": stimulus_ids,"solution_ids": solution_ids}