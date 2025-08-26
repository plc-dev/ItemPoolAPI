from enum import Enum
from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ------------------------
# ENUMS
# ------------------------
class TaskType(str, Enum):
    sql = "sql"


class MaterialType(str, Enum):
    database = "database"


# ------------------------
# REQUEST MODELS
# ------------------------
class TaskMaterial(BaseModel):
    type: MaterialType
    material_information: Dict[str, Any]


class Task(BaseModel):
    task_description: str
    task_material_ids: List[int]
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
    material_ids: List[int]
    solutions: List[str]
    result: Dict[str, Any]


# ------------------------
# MOCK DATABASE
# ------------------------
materials_db: Dict[int, TaskMaterial] = {}
tasks_db: List[Dict[str, Any]] = []
material_counter = 0


# ------------------------
# ENDPOINTS
# ------------------------
@app.post("/registerTaskMaterial", response_model=RegisterTaskMaterialResponse)
async def register_task_material(task_material: TaskMaterial):
    global material_counter
    material_counter += 1

    materials_db[material_counter] = task_material

    # Hier können Metadaten für die Filterung berechnet werden

    return RegisterTaskMaterialResponse(id=material_counter)


@app.post("/registerTask", response_model=RegisterTaskResponse)
async def register_task(request: RegisterTaskRequest):
    task_type = request.type
    material_ids = request.task.task_material_ids
    solutions = request.task.task_solutions

    # Hier können Metadaten für die Filterung berechnet werden

    # Validate that all referenced IDs exist
    missing_ids = [mid for mid in material_ids if mid not in materials_db]
    if missing_ids:
        return RegisterTaskResponse(
            status="error",
            task_type=task_type,
            material_ids=material_ids,
            solutions=solutions,
            result={"error": f"Invalid material IDs: {missing_ids}"},
        )

    match task_type:
        case TaskType.sql:
            result = {
                "note": "SQL task registered",
                "solutions_count": len(solutions),
            }
        case _:
            result = {"note": "Unknown task type"}

    # Store task
    task_entry = {
        "type": task_type,
        "material_ids": material_ids,
        "solutions": solutions,
    }
    tasks_db.append(task_entry)

    return RegisterTaskResponse(
        status="success",
        task_type=task_type,
        material_ids=material_ids,
        solutions=solutions,
        result=result,
    )

@app.get("/enums", summary="Get all enums for task and material types")
def get_enums():
    """
    Returns the available task and material types for the frontend to use in dropdowns.
    """
    return {
        "task_types": [t.value for t in TaskType],
        "material_types": [m.value for m in MaterialType],
    }

