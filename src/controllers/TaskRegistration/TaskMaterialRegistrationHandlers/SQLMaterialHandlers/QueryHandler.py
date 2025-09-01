from ..BaseHandler import TaskMaterialHandler
from .....models.Task import QueryTaskMaterial, Metadata

from ....MetaDataInference.SQLDataInferenceHandlers.QueryMetaDataInferenceHandler import QueryMetricsHandler

class QueryMaterialHandler(TaskMaterialHandler):
    def __init__(self, dao):
        super().__init__(dao)

    # TODO: Specify QueryMetadata type
    def process_material(self, material: QueryTaskMaterial) -> Metadata:
        query_meta_data_inference_handler = QueryMetricsHandler()

        meta_data = query_meta_data_inference_handler.infer_metadata(material.query)

        return meta_data