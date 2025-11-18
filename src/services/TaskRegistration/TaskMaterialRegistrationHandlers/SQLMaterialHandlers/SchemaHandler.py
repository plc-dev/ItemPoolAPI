from ..BaseHandler import TaskMaterialHandler
from .....models.Tasks.BaseTask import Metadata
from .....models.TaskMaterials.SchemaTaskMaterial import SchemaTaskMaterial

from ....MetaDataInference.SQLDataInferenceHandlers.SchemaMetaDataInferenceHandler import (
    SchemaMetricsHandler,
)


class SchemaMaterialHandler(TaskMaterialHandler):
    def __init__(self, dao):
        super().__init__(dao)

    # TODO: Specify ScehmaMetadata type
    def process_material(self, material: SchemaTaskMaterial) -> Metadata:
        schema_meta_data_inference_handler = SchemaMetricsHandler()

        meta_data = schema_meta_data_inference_handler.infer_metadata(material.schema)

        return meta_data
