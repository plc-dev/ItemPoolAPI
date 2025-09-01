from ..BaseHandler import TaskMaterialHandler
from .....models.Task import TextTaskMaterial, Metadata

from ....MetaDataInference.TextMetaDataInferenceHandlers.TextMetricsHandler import TextMetricsHandler

class TextMaterialHandler(TaskMaterialHandler):
    def __init__(self, dao):
        super().__init__(dao)

    # TODO: Specify TextMetadata type
    def process_material(self, material: TextTaskMaterial) -> Metadata:
        text_meta_data_inference_handler = TextMetricsHandler()

        meta_data = text_meta_data_inference_handler.infer_metadata(material.text)

        return meta_data