from abc import ABC, abstractmethod
#from ....models.Task import Task, MaterialIdOrMaterialReqestObject, TaskMaterial, TaskMaterialRegistrationRequestObject

from ....models.Task import (
    Task,
    MaterialIdOrMaterialReqestObject,
    TaskMaterial,
    TaskMaterialRegistrationRequestObject,
    # Für robustes Wrapping:
    MaterialType,
    DatabaseDialects,
    TextTaskMaterial,
    QueryTaskMaterial,
    SchemaTaskMaterial,
    DatabaseTaskMaterial,
    TextMaterialRegistrationRequestObject,
    QueryMaterialRegistrationRequestObject,
    SchemaMaterialRegistrationRequestObject,
    DatabaseRegistrationRequestObject,
)


from ....models.Error import RecordNotFoundError
from ....database.DAO import DAO
#from typing import List, Dict
from typing import List, Any

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
    
    def _is_single_material(self, material):
        return not isinstance(material, list)
    
    def _handle_id(self, id: int):
        result = self._dao.get_task_material(id)
        
        if result == None:
            raise RecordNotFoundError(f"The task_material_id: {id} does not exist.")
        return id
        
    def _handle_id_or_material(self, id_or_material: MaterialIdOrMaterialReqestObject) -> int:
        """
        Akzeptiert:
          - int (bereits existierende Material-ID)
          - dict im Endpunkt-Format: {"type": "...", "material_information": {...}}
          - dict "roh": z.B. {"query": "...", "dialect": "postgres"} o. {"text": "..."} etc.
          - Pydantic-Objekte (TextTaskMaterial, QueryTaskMaterial, ...)
        Baut bei Bedarf das passende *MaterialRegistrationRequestObject*.
        """
        if self._is_id(id_or_material):
            return self._handle_id(id_or_material)

        material = id_or_material

        # 1) Bereits im API-Format? (type + material_information vorhanden)
        if isinstance(material, dict) and "type" in material and "material_information" in material:
            req = TaskMaterialRegistrationRequestObject(**material)
            return self._task_material_controller.register_material(req)

        # 2) Rohes DICT für Query?
        if isinstance(material, dict) and "query" in material and "dialect" in material:
            req = QueryMaterialRegistrationRequestObject(
                material_information=QueryTaskMaterial(
                    query=material["query"],
                    dialect=DatabaseDialects(material["dialect"]),
                    metadata=None,
                )
            )
            return self._task_material_controller.register_material(req)

        # 3) Rohes DICT für Text?
        if isinstance(material, dict) and "text" in material:
            req = TextMaterialRegistrationRequestObject(
                material_information=TextTaskMaterial(text=material["text"], metadata=None)
            )
            return self._task_material_controller.register_material(req)

        # 4) Rohes DICT für Schema?
        if isinstance(material, dict) and "schema" in material and "name" in material:
            req = SchemaMaterialRegistrationRequestObject(
                material_information=SchemaTaskMaterial(
                    schema=material.get("schema") or "",
                    name=material["name"],
                    metadata=None,
                )
            )
            return self._task_material_controller.register_material(req)

        # 5) Rohes DICT für Database?
        if isinstance(material, dict) and "database" in material and "name" in material and "dialect" in material:
            req = DatabaseRegistrationRequestObject(
                material_information=DatabaseTaskMaterial(
                    database=material.get("database") or "",
                    name=material["name"],
                    dialect=DatabaseDialects(material["dialect"]),
                    metadata=None,
                )
            )
            return self._task_material_controller.register_material(req)

        # 6) Pydantic-Objekte (bereits modelliert, aber ohne 'type')
        if isinstance(material, QueryTaskMaterial):
            req = QueryMaterialRegistrationRequestObject(material_information=material)
            return self._task_material_controller.register_material(req)
        if isinstance(material, TextTaskMaterial):
            req = TextMaterialRegistrationRequestObject(material_information=material)
            return self._task_material_controller.register_material(req)
        if isinstance(material, SchemaTaskMaterial):
            req = SchemaMaterialRegistrationRequestObject(material_information=material)
            return self._task_material_controller.register_material(req)
        if isinstance(material, DatabaseTaskMaterial):
            req = DatabaseRegistrationRequestObject(material_information=material)
            return self._task_material_controller.register_material(req)

        # 7) Letzter Fallback: hart als Text behandeln
        req = TextMaterialRegistrationRequestObject(
            material_information=TextTaskMaterial(text=str(material), metadata=None)
        )
        return self._task_material_controller.register_material(req)
    
    def _register_materials(self, materials: MaterialIdOrMaterialReqestObject | List[MaterialIdOrMaterialReqestObject]) -> List[int]:
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
    def process_task(self, task: Task) -> dict[str, Any]:
        raise NotImplementedError