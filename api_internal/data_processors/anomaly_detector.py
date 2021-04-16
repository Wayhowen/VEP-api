import traceback

from data_preprocessors.gait_features_extractor.extractor import Extractor as GaitFeaturesExtractor
from data_processors.base_processor import BaseProcessor


class AnomalyDetector(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.gait_features_extractor = GaitFeaturesExtractor()

    def _preprocess_data(self, data):
        try:
            gait_features = self.gait_features_extractor.extract_features(data["ACCELEROMETER"]["ACCELEROMETER_TIMES"],
                                                                          data["ACCELEROMETER"]["ACCELEROMETER_x"],
                                                                          data["ACCELEROMETER"]["ACCELEROMETER_y"],
                                                                          data["ACCELEROMETER"]["ACCELEROMETER_z"])
        except Exception as e:
            print(f"{e} exception while extracting features")
            print(traceback.print_exc())
            return None
        print(gait_features)
        return gait_features

    def _process_data(self, data):
        return data
