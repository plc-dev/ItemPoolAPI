from ..BaseMetaDataInferenceHandler import MetaDataInferenceHandler

class DatabaseMetricsHandler(MetaDataInferenceHandler):
    """
    TODO
    """
    def __init__(self):
        super().__init__()

    def infer_metadata(self, database: str):
        return super().infer_metadata(database)