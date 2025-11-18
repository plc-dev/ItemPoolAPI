from pydantic import BaseModel
from typing import Literal


class Origin(BaseModel):
    organisation: str
    person: str
    role: Literal["professor", "staff", "student"]
