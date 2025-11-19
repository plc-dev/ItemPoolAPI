from enum import Enum
from .BaseTaskMaterial import Metadata, TaskMaterial, MaterialType
from typing import Optional
from pydantic import BaseModel


class DatabaseDialects(str, Enum):
    postgres = "postgres"
    sqlite = "sqlite"
    oracle = "oracle"


class QueryMetadata(Metadata):
    pass


class QueryTaskMaterial(TaskMaterial):
    query: str
    dialect: DatabaseDialects
    metadata: Optional[QueryMetadata]


class QueryMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType.query
    material_information: QueryTaskMaterial
