from ..BaseMetaDataInferenceHandler import MetaDataInferenceHandler
# import 

class TextMetricsHandler(MetaDataInferenceHandler):
    """
    Wraps the textstat python library and calculates all its available metrics for the passed text.
    """
    def __init__(self):
        super().__init__()

    def infer_metadata(self, text: str):
        return super().infer_metadata(text)