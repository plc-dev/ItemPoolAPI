from ..TaskMaterials.BaseTaskMaterial import TaskMaterial, MaterialType
from pydantic import BaseModel


class SchemaTaskMaterial(TaskMaterial):
    # TODO: Specify further? Could be potentially a graph, a picture, a table, etc. (which technically can all be expressed as a string)
    schema: str
    name: str


class SchemaMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType.schema
    material_information: SchemaTaskMaterial
