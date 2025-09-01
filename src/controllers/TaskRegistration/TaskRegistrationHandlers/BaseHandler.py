from abc import ABC, abstractmethod
from ....models.Task import Task, MaterialIdOrMaterialReqestObject, TaskMaterial, TaskMaterialRegistrationRequestObject
from ....models.Error import RecordNotFoundError
from ....database.DAO import DAO
from typing import List, Dict

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
        return not isinstance(material, list)
    
    def _handle_id(self, id: int):
        result = self._dao.get_task_material(id)
        
        if result == None:
            raise RecordNotFoundError(f"The task_material_id: {id} does not exist.")
        return id
        
    def _handle_id_or_material(self, id_or_material: MaterialIdOrMaterialReqestObject):
        if self._is_id(id_or_material):
            id = self._handle_id(id_or_material)
        else:
            material = id_or_material
            id = self._task_material_controller.register_material(TaskMaterialRegistrationRequestObject(**material))
        return id
    
    def _register_materials(self, materials: MaterialIdOrMaterialReqestObject | List[MaterialIdOrMaterialReqestObject]) -> Dict:
        """
        This method registers any task material via the TaskMaterialRegistrationController.
        TODO: Wrap the registration of subsequent materials into a transaction that aborts on error to avoid partial write operations of materials which may be duplicated in follow up requests.
        """
        if self._is_single_material(materials):
            id = self._handle_id_or_material(materials)
            return [id]
        else:
            material_ids = []
            for material in materials:
                id = self._handle_id_or_material(material)
                material_ids.append(id)
                return material_ids

    @abstractmethod
    def process_task(self, task: Task) -> Dict:
        return