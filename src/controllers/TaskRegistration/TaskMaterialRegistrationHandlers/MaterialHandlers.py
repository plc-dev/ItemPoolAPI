from .BaseHandler import TaskMaterialHandler
from ....models.Task import MaterialType

from .GeneralHandlers.TextHandler import TextMaterialHandler
from .SQLMaterialHandlers.QueryHandler import QueryMaterialHandler
from .SQLMaterialHandlers.DatabaseHandler import DatabaseMaterialHandler
from .SQLMaterialHandlers.SchemaHandler import SchemaMaterialHandler

material_handlers: dict[str, TaskMaterialHandler] = {
    MaterialType.text: TextMaterialHandler,
    MaterialType.query: QueryMaterialHandler,
    MaterialType.schema: SchemaMaterialHandler,
    MaterialType.database: DatabaseMaterialHandler,
}