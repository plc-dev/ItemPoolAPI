from typing import List
from pydantic import BaseModel


class TaskCollectionCreationRequestObject(BaseModel):
    task_collection: List[int]
    task_collection_name: str
