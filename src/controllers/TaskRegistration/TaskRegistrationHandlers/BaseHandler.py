from abc import ABC, abstractmethod
from ....models.Task import Task, MaterialIdOrMaterialReqestObject, TaskMaterial
from ....models.Error import RecordNotFoundError
from ....database.DAO import DAO
from typing import List, Dict
from collections.abc import Iterable
import logging

# TODO: Refactor controllers to avoid circular imports
# from ..TaskRegistrationController import TaskMaterialRegistrationController

class TaskHandler(ABC):
    """
    This class processes tasks generically
    """
    def __init__(self, dao: DAO, task_material_controller):
        self._dao = dao
        self._task_material_controller = task_material_controller

    def _is_id(self, id_or_material: MaterialIdOrMaterialReqestObject):
        if isinstance(id_or_material, int):
            return True
        return False
    
    def _is_single_material(self, material: TaskMaterial):
        return not isinstance(material, Iterable)
    
    def _register_materials(self, materials: MaterialIdOrMaterialReqestObject | List[MaterialIdOrMaterialReqestObject]):
        """
        This method registers any task material via the TaskMaterialRegistrationController.
        TODO: Wrap the registration of subsequent materials into a transaction that aborts on error to avoid partial write operations of materials which may be duplicated in follow up requests.
        """
        
        logger = logging.getLogger('uvicorn.error')
        logger.info("ERR:")
        logger.info(materials)

        material_ids = {}
        for material_name, id_or_material in materials.items():
            if self._is_id(id_or_material):
                id = id_or_material
                result = self._dao.get_task_material(id_or_material)
                
                if result == None:
                    raise RecordNotFoundError(f"The task_material_id: {id} does not exist.")

                material_ids[material_name] = id
            else:
                materials = id_or_material
                if self._is_single_material(materials):
                    material = materials
                    id = self._task_material_controller.register_material(material)
                    material_ids[material_name] = id
                else:
                    for material in materials:
                        id = self._task_material_controller.register_material(material)
                        material_ids[material_name] = id
        return material_ids

    @abstractmethod
    def process_task(self, task: Task) -> Dict:
        return