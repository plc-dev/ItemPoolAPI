from ..models.Tasks.BaseTask import (
    TaskRegistrationResponse,
    TaskRegistrationRequestObject,
)

from ..services.TaskRegistration.TaskRegistrationService import (
    TaskRegistrationService,
    TaskMaterialRegistrationService,
)
from ..models.Tasks.BaseTask import (
    TaskType,
    ResponseStatus,
    ResponseResult,
)
from ..models.TaskMaterials.BaseTaskMaterial import (
    MaterialType,
    TaskMaterialRegistrationRequestObject,
    TaskMaterialRegistrationResponseObject,
)
from fastapi import APIRouter

router = APIRouter()


@router.get("/availableMaterialTypes")
async def get_available_material_types():
    return [k.value for k in MaterialType]


@router.get("/availableTaskTypes")
async def get_available_task_types():
    return [k.value for k in TaskType]


@router.post(
    "/registerTaskMaterial", response_model=TaskMaterialRegistrationResponseObject
)
async def register_task_material_route(request: TaskMaterialRegistrationRequestObject):
    task_material_registration_service = TaskMaterialRegistrationService()
    id = task_material_registration_service.register_material(request)
    return TaskMaterialRegistrationResponseObject(id=id)


@router.post("/registerTask", response_model=TaskRegistrationResponse)
async def register_task_route(request: TaskRegistrationRequestObject):
    if request.type not in TaskType:
        return TaskRegistrationResponse(
            status=ResponseStatus.error,
            id=None,
            task_type=request.type,
            stimulus=request.task.task_stimulus,
            solutions=request.task.task_solutions,
            result=ResponseResult(message=f"Invalid task type: {request.type}"),
        )

    task_registration_service = TaskRegistrationService()
    response = task_registration_service.register_task(request)

    return TaskRegistrationResponse(**response, task_type=request.type)
