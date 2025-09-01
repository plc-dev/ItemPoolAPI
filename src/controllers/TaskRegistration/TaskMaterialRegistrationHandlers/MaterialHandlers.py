from .BaseHandler import TaskMaterialHandler
from ....models.Task import MaterialType

from .GeneralHandlers.TextHandler import TextMaterialHandler

material_handlers: dict[str, TaskMaterialHandler] = {
    MaterialType.text: TextMaterialHandler
}