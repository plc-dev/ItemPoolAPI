from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional, Union


class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow")


class TaskMaterial(BaseModel):
    model_config = ConfigDict(extra="allow")
    metadata: Optional[Metadata]


class MaterialType(str, Enum):
    database = "database"
    query = "query"
    problem_statement = "problem_statement"
    schema = "schema"
    text = "text"


class TaskMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType
    material_information: TaskMaterial


MaterialIdOrMaterialReqestObject = Union[int, TaskMaterialRegistrationRequestObject]


class TaskMaterialRegistrationResponseObject(BaseModel):
    id: int
