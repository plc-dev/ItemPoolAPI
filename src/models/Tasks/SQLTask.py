from .BaseTask import (
    TaskStimulus,
    TaskSolutions,
    Task,
    TaskRegistrationRequestObject,
    TaskType,
)
from ..TaskMaterials.QueryTaskMaterial import QueryTaskMaterial
from ..TaskMaterials.InstructionTaskMaterial import InstructionTaskMaterial
from ..TaskMaterials.TextTaskMaterial import TextTaskMaterial
from ..TaskMaterials.SchemaTaskMaterial import SchemaTaskMaterial
from ..TaskMaterials.DatabaseTaskMaterial import DatabaseTaskMaterial
from typing import List


class SQLTaskStimulus(TaskStimulus):
    """
    Stimulus for a task, in which a learner is instructed to write an SQL-query that matches a natural-language problem statement.
    """

    instruction: List[InstructionTaskMaterial | int]
    problem_statement: List[TextTaskMaterial | int]
    db_schema: SchemaTaskMaterial | int
    database: DatabaseTaskMaterial | int


class SQLTaskSolution(TaskSolutions):
    query: List[QueryTaskMaterial]


class SQLTask(Task):
    task_stimulus: SQLTaskStimulus
    task_solutions: SQLTaskSolution


class SQLTaskRegistrationRequestObject(TaskRegistrationRequestObject):
    type: TaskType.sql
    task: SQLTask
