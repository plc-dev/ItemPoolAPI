
from ..models.Task import TaskMaterialRegistrationResponse, TaskRegistrationResponse, TaskRegistrationRequestObject, TaskMaterialRegistrationRequestObject
from ..controllers.TaskRegistration.TaskRegistrationController import TaskRegistrationController, TaskMaterialRegistrationController
from ..models.Task import TaskType, MaterialType, ResponseStatus, ResponseResult
import logging
from fastapi import APIRouter

router = APIRouter()

@router.get("/availableMaterialTypes")
async def get_available_material_types():
    return [k.value for k in MaterialType]

@router.get("/availableTaskTypes")
async def get_available_task_types():
    return [k.value for k in TaskType]

@router.post("/registerTaskMaterial", response_model=TaskMaterialRegistrationResponse)
async def register_task_material_route(request: TaskMaterialRegistrationRequestObject):
    controller = TaskMaterialRegistrationController()
    id = controller.register_material(request)
    return TaskMaterialRegistrationResponse(id=id)

@router.post("/registerTask", response_model=TaskRegistrationResponse)
async def register_task_route(request: TaskRegistrationRequestObject):
    if request.type not in TaskType:
        return TaskRegistrationResponse(
            status = ResponseStatus.error,
            id = None,
            task_type = request.type,
            stimulus = request.task.task_stimulus,
            solutions = request.task.task_solutions,
            result = ResponseResult(message = f"Invalid task type: {request.type}")
        )

    controller = TaskRegistrationController()
    response = controller.register_task(request)

    return TaskRegistrationResponse(**response, task_type=request.type)