from typing import Dict, Any
from enum import Enum
from pymongo import MongoClient, ReturnDocument
import os

class Collections(Enum):
    TASK_MATERIAL = "materials"
    TASK = "tasks"
    COUNTER = "counters"

class DAO:
    __client: MongoClient
    __db: Any

    def __init__(self):
        MONGO_USER = os.getenv("MONGO_USER")
        MONGO_PW = os.getenv("MONGO_PW")
        MONGO_DB = os.getenv("MONGO_DB")
        MONGO_PORT = os.getenv("MONGO_PORT")
        MONGO_HOST = os.getenv("MONGO_HOST")

        self.__client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PW}@{MONGO_HOST}:{MONGO_PORT}/")
        self.__db = self.__client[MONGO_DB]
        pass
    
    def _get_collection(self, col_name: str):
        return self.__db[col_name]
    
    def _get_next_seq(self, collection_name: str) -> int:
        col = self._get_collection(Collections.COUNTER)

        doc = col.find_one_and_update(
            {"_id": collection_name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        if "seq" not in doc:
            col.update_one({"_id": collection_name}, {"$set": {"seq": 1}})
            return 1
        return int(doc["seq"])

    def _isPydanticObject(self, obj: Any) -> bool:
        return hasattr(obj, "model_dump")

    # ---------- TaskMaterial ----------
    def store_task_material(self, material_obj: dict) -> int | None:
        new_id = self._get_next_seq(Collections.TASK_MATERIAL)
        
        material_obj["_id"] = new_id
        materials_col = self._get_collection(Collections.TASK_MATERIAL)
        materials_col.replace_one({"_id": new_id}, material_obj, upsert=True)
        return new_id

    def get_task_material(self, id: int):
        materials_col = self._get_collection(Collections.TASK_MATERIAL)
        doc = materials_col.find_one({"_id": int(id)})
        return doc

    # ---------- Task ----------
    def store_task(self, task: Dict) -> int | None:
        new_id = self._get_next_seq(Collections.TASK)
        doc = {
            "_id": new_id,
            "stimulus_ids": task["stimulus_ids"],
            "solution_ids": task["solution_ids"],
        }
        tasks_col = self._get_collection(Collections.TASK)
        tasks_col.replace_one({"_id": new_id}, doc, upsert=True)
        return new_id

dao = DAO()
