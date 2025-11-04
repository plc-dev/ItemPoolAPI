# src/database/DAO.py
from typing import Dict, Any
from pymongo import MongoClient, ReturnDocument
import os

# ----- Verbindung und DB wählen -----
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "itempool")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

materials_col = db["materials"]
tasks_col = db["tasks"]
counters_col = db["counters"]

def _get_next_seq(name: str) -> int:
    """
    Erhöht (oder legt an) einen Zähler in 'counters' und gibt den nächsten int-Wert zurück.
    """
    doc = counters_col.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    # Beim allerersten Mal hat 'seq' evtl. noch nicht existiert -> standardisiere auf 1
    if "seq" not in doc:
        counters_col.update_one({"_id": name}, {"$set": {"seq": 1}})
        return 1
    return int(doc["seq"])

class DAO:
    """
    Mongo-basierter DAO mit der gleichen öffentlichen API wie die frühere In-Memory-Version.
    """

    def __init__(self):
        # Nichts weiter nötig; Collections stehen oben bereit
        pass

    # ---------- TaskMaterial ----------
    def store_task_material(self, material_obj) -> int | None:
        """
        Erwartet ein Pydantic-Objekt oder dict.
        Speichert unter integer _id und gibt diese zurück.
        """
        new_id = _get_next_seq("materials")

        # Pydantic -> dict
        if hasattr(material_obj, "model_dump"):
            doc: Dict[str, Any] = material_obj.model_dump()
        else:
            doc = dict(material_obj)

        doc["_id"] = new_id
        materials_col.replace_one({"_id": new_id}, doc, upsert=True)
        return new_id

    def get_task_material(self, id: int):
        """
        Holt ein Material-Dokument per integer _id.
        """
        doc = materials_col.find_one({"_id": int(id)})
        # Rückgabe wie vorher: das gespeicherte Objekt (dict). Falls du hier Pydantic wünschst, kannst du es rekonstruieren.
        return doc

    # ---------- Task ----------
    def store_task(self, task: Dict) -> int | None:
        """
        Speichert den kompakten Task:
          {
            "stimulus_ids": Dict[str, List[int]],
            "solution_ids": Dict[str, List[int]]
          }
        """
        new_id = _get_next_seq("tasks")
        doc = {
            "_id": new_id,
            "stimulus_ids": task["stimulus_ids"],
            "solution_ids": task["solution_ids"],
        }
        tasks_col.replace_one({"_id": new_id}, doc, upsert=True)
        return new_id

# Singleton-Instanz wie zuvor
dao = DAO()
