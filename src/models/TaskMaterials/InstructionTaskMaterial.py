from pydantic import BaseModel, ConfigDict
from .TextTaskMaterial import TextTaskMaterial
from typing import Optional, List
from .BaseTaskMaterial import TaskMaterialRegistrationRequestObject, MaterialType


class InstructionalConstraint(BaseModel):
    model_config = ConfigDict(extra="allow")


class InstructionTaskMaterial(TextTaskMaterial):
    constraints: Optional[List[InstructionalConstraint]]


class TextMaterialRegistrationRequestObject(TaskMaterialRegistrationRequestObject):
    type: MaterialType.text
    material_information: InstructionTaskMaterial
