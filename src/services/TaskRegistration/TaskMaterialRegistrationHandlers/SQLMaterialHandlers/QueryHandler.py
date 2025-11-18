from ..BaseHandler import TaskMaterialHandler
from .....models.TaskMaterials.QueryTaskMaterial import QueryTaskMaterial, QueryMetadata

from ....MetaDataInference.SQLDataInferenceHandlers.QueryMetaDataInferenceHandler import (
    QueryMetricsHandler,
)


class QueryMaterialHandler(TaskMaterialHandler):
    def __init__(self, dao):
        super().__init__(dao)

    # TODO: Specify QueryMetadata type in Task.py
    # TODO: Include schema (if available)? => Allows for qualifying the query (mapping table identifiers to a schema). In turn allows for lineage tracing etc.
    def process_material(self, material: QueryTaskMaterial) -> QueryMetadata:
        query_meta_data_inference_handler = QueryMetricsHandler()

        meta_data = query_meta_data_inference_handler.infer_metadata(material)

        return meta_data
