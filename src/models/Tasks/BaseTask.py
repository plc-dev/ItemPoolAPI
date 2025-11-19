from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import List, Union, Literal, Optional, Dict


class TaskType(str, Enum):
    sql = "sql"


class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow")


class TaskStimulus(BaseModel):
    model_config = ConfigDict(extra="allow")


class TaskSolutions(BaseModel):
    model_config = ConfigDict(extra="allow")


class TaskMetadata(Metadata):
    name: str


class Task(BaseModel):
    task_stimulus: TaskStimulus
    task_solutions: TaskSolutions
    metadata: Optional[TaskMetadata]


class TaskRegistrationRequestObject(BaseModel):
    type: TaskType
    task: Task


class ResponseStatus(str, Enum):
    success = "success"
    error = "error"


class ResponseResult(BaseModel):
    message: str


class TaskRegistrationResponse(BaseModel):
    status: ResponseStatus
    id: int
    task_type: TaskType
    stimulus_ids: Dict[str, List[int]]
    solution_ids: Dict[str, List[int]]
    metadata: TaskMetadata
    result: ResponseResult
