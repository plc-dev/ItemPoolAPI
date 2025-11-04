from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import List, Union, Literal, Optional, Dict


# ------------------------
# BASE MODELS
# ------------------------
class TaskType(str, Enum):
    sql = "sql"

class MaterialType(str, Enum):
    database = "database"
    query = "query"
    problem_statement = "problem_statement"
    schema = "schema"
    text = "text"

class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow")

class TaskMaterial(BaseModel):
    model_config = ConfigDict(extra="allow")
    metadata: Optional[Metadata] = None

# ------------------------
# ORIGIN TYPE
# ------------------------
# TODO: How to model the origin of a task (materials)?
class Origin(BaseModel):
    organisation: str
    person: str
    role: Literal["professor", "staff", "student"]


# ------------------------
# REQUEST MODELS
# ------------------------
class TaskMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType
    material_information: TaskMaterial

class SolutionRegistrationRequestObject(TaskMaterialRegistrationRequestObject):
    # TODO: Think about design implications and potentially refactor. 
    # For the current purposes, the solution may be the treated the same as other task-materials?
    pass

MaterialIdOrMaterialReqestObject = Union[int, TaskMaterialRegistrationRequestObject]

class TaskStimulus(BaseModel):
    model_config = ConfigDict(extra="allow")

class TaskSolutions(BaseModel):
    model_config = ConfigDict(extra="allow")

class Task(BaseModel):
    task_stimulus: TaskStimulus
    task_solutions: TaskSolutions

class TaskRegistrationRequestObject(BaseModel):
    type: TaskType
    task: Task

# ------------------------
# RESPONSE MODELS
# ------------------------
class TaskMaterialRegistrationResponse(BaseModel):
    id: int

class ResponseStatus(str, Enum):
    success = "success"
    error = "error"

class ResponseResult(BaseModel):
    message: str


class TaskRegistrationResponse(BaseModel):
    status: ResponseStatus
    id: int
    task_type: TaskType
    stimulus_ids: Dict[str,List[int]]
    solution_ids: Dict[str,List[int]]
    result: ResponseResult

# ------------------------
# GENERAL TASK ELEMENTS
# ------------------------
class TextTaskMaterial(TaskMaterial):
    text: str

class TextMetadata(Metadata):
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    smog_index: float
    coleman_liau_index: float
    automated_readability_index: float
    dale_chall_readability_score: float
    difficult_words: float
    linsear_write_formula: float
    gunning_fog: float
    text_standard: float
    fernandez_huerta: float
    szigriszt_pazos: float
    gutierrez_polini: float
    crawford: float
    gulpease_index: float
    osman: float


class InstructionalConstraint(BaseModel):
    model_config = ConfigDict(extra="allow")
    
class TaskInstruction(TextTaskMaterial):
    constraints: Optional[List[InstructionalConstraint]]

class TextMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType
    material_information: TextTaskMaterial | TaskInstruction

# ------------------------
# SQL TASK SPECIFIC ELEMENTS
# ------------------------
class DatabaseDialects(str, Enum):
    postgres = "postgres"
    sqlite = "sqlite"
    oracle = "oracle"


class QueryMetadata(Metadata):
    pass
class QueryTaskMaterial(TaskMaterial):
    query: str
    dialect: DatabaseDialects
    metadata: Optional[QueryMetadata] = None

class QueryMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType
    material_information: QueryTaskMaterial

class SchemaTaskMaterial(TaskMaterial):
    # TODO: Specify further? Could be potentially a graph, a picture, a table, etc. (which technically can all be expressed as a string)
    schema: str
    name: str

class SchemaMaterialRegistrationRequestObject(BaseModel):
    type: MaterialType
    material_information: SchemaTaskMaterial

class DatabaseTaskMaterial(TaskMaterial):
    database: str
    name: str
    dialect: DatabaseDialects

class DatabaseRegistrationRequestObject(BaseModel):
    type: MaterialType
    material_information: DatabaseTaskMaterial


class SQLTaskStimulus(TaskStimulus):
    """
    Stimulus for a task, in which a learner is instructed to write an SQL-query that matches a natural-language problem statement.
    """
    instruction: List[TaskInstruction | int]
    problem_statement: List[TextTaskMaterial | int]
    #db_schema: SchemaMaterialRegistrationRequestObject | int
    db_schema: SchemaTaskMaterial | int
    database: DatabaseTaskMaterial | int

class SQLTaskSolution(TaskSolutions):
    query: List[QueryTaskMaterial]

class SQLTask(Task):
    task_stimulus: SQLTaskStimulus
    task_solutions: SQLTaskSolution

class SQLTaskRegistrationRequestObject(TaskRegistrationRequestObject):
    type: TaskType
    task: SQLTask


# --- ensure forward ref resolution (pydantic v2) ---
TextMaterialRegistrationRequestObject.model_rebuild()
QueryMaterialRegistrationRequestObject.model_rebuild()
SchemaMaterialRegistrationRequestObject.model_rebuild()
DatabaseRegistrationRequestObject.model_rebuild()

SQLTaskRegistrationRequestObject.model_rebuild()
TaskRegistrationRequestObject.model_rebuild()
