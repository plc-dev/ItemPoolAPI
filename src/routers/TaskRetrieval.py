
from fastapi import APIRouter
from ..database.DAO import dao

router = APIRouter()

@router.get("/fetchMaterialFromId")
async def fetch_material_from_id(id: int):
    return dao.get_task_material(id)