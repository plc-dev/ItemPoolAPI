from .BaseTaskMaterial import TaskMaterial, MaterialType
from .QueryTaskMaterial import DatabaseDialects
from pydantic import BaseModel


class DatabaseTaskMaterial(TaskMaterial):
    database: str
    name: str
    dialect: DatabaseDialects


class DatabaseRegistrationRequestObject(BaseModel):
    type: MaterialType.database
    material_information: DatabaseTaskMaterial
