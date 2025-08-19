from enum import Enum
from typing import Any, Dict, List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ------------------------
# ENUMS
# ------------------------
class TaskType(str, Enum):
    database = "database"
    sql = "sql"


class MaterialType(str, Enum):
    task_description = "task_description"
    schema_description = "schema_description"
    resolve_existing_material = "resolve_existing_material"
    database = "database"
    sql = "sql"


# ------------------------
# REQUEST MODELS
# ------------------------
class TaskMaterialBase(BaseModel):
    type: MaterialType


class TaskMaterial(TaskMaterialBase):
    material_information: Dict[str, Any]


class TaskMaterialReference(TaskMaterialBase):
    id: str


TaskMaterialType = Union[TaskMaterial, TaskMaterialReference]


class Task(BaseModel):
    task_material: List[TaskMaterialType]
    task_solutions: List[str]


class RegisterTaskRequest(BaseModel):
    type: TaskType
    task: Task


# ------------------------
# RESPONSE MODELS
# ------------------------
class RegisterTaskMaterialResponse(BaseModel):
    id: int


class RegisterTaskResponse(BaseModel):
    status: str
    task_type: TaskType
    materials: List[Dict[str, Any]]
    solutions: List[str]
    result: Dict[str, Any]


# ------------------------
# ENDPOINTS
# ------------------------
@app.post("/registerTaskMaterial", response_model=RegisterTaskMaterialResponse)
async def register_task_material(task_material: TaskMaterial):
    # TODO: hier könnte das Material gespeichert werden
    return RegisterTaskMaterialResponse(id=0)


@app.post("/registerTask", response_model=RegisterTaskResponse)
async def register_task(request: RegisterTaskRequest):
    task_type = request.type
    materials = request.task.task_material
    solutions = request.task.task_solutions

    match task_type:
        case TaskType.sql:
            result = {
                "note": "SQL task registered",
                "solutions_count": len(solutions),
            }
        case TaskType.database:
            result = {
                "note": "Database task registered",
                "materials_count": len(materials),
            }
        case _:
            result = {"note": "Unknown task type"}

    return RegisterTaskResponse(
        status="success",
        task_type=task_type,
        materials=[m.dict() for m in materials],
        solutions=solutions,
        result=result,
    )
