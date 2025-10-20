from ..BaseHandler import TaskMaterialHandler
from .....models.Task import DatabaseTaskMaterial, Metadata

from ....MetaDataInference.SQLDataInferenceHandlers.DatabaseMetaDataInferenceHandler import DatabaseMetricsHandler

class DatabaseMaterialHandler(TaskMaterialHandler):
    def __init__(self, dao):
        super().__init__(dao)

    # TODO: Specify DatabaseMetadata type
    def process_material(self, material: DatabaseTaskMaterial) -> Metadata:
        database_meta_data_inference_handler = DatabaseMetricsHandler()

        meta_data = database_meta_data_inference_handler.infer_metadata(material.database)

        return meta_data