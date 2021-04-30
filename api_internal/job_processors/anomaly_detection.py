from data_preprocessors.gait_features_extractor.extractor import Extractor as GaitFeaturesExtractor
from job_processors.base_processor import BaseProcessor


class AnomalyDetector(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.gait_features_extractor = GaitFeaturesExtractor()

    def _preprocess_data(self, data, *args, **kwargs):
        return data

    def _process_data(self, data, *args, **kwargs):
        return data
