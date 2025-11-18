from .BaseHandler import TaskHandler
from ....models.Task import SQLTask, ResponseStatus, ResponseResult

import logging


class SQLTaskHandler(TaskHandler):
    def __init__(self, dao, task_material_controller):
        super().__init__(dao, task_material_controller)

    def process_task(self, task: SQLTask):
        try:
            instruction_ids = self._register_materials(task.task_stimulus.instruction)
            problem_statement_ids = self._register_materials(
                task.task_stimulus.problem_statement
            )
            schema_ids = self._register_materials(task.task_stimulus.db_schema)
            database_ids = self._register_materials(task.task_stimulus.database)

            stimulus_ids = {
                "instruction_ids": instruction_ids,
                "problem_statement_ids": problem_statement_ids,
                "schema_ids": schema_ids,
                "database_ids": database_ids,
            }

            query_ids = self._register_materials(task.task_solutions.query)

            solution_ids = {"query_ids": query_ids}

            return {
                "status": ResponseStatus.success,
                "stimulus_ids": stimulus_ids,
                "solution_ids": solution_ids,
                "metadata": task.metadata,
                "result": ResponseResult(message="Task successfully registered"),
            }

        except Exception as e:
            logging.getLogger("uvicorn.error").error(e)
            return {
                "status": ResponseStatus.error,
                "result": ResponseResult(message=str(e)),
                "stimulus_ids": {},
                "solution_ids": {},
            }
