import traceback

import settings
from data_preprocessors.gait_features_extractor.extractor import Extractor as GaitFeaturesExtractor
from data_processors.fuzzy_logic_processor.fuzzy_system_controller import FuzzySystemController
from job_processors.base_processor import BaseProcessor


class PatientExerciseEvaluator(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.gait_features_extractor = GaitFeaturesExtractor()
        self.fuzzy_logic_evaluator = FuzzySystemController()

        self._fuzzy_download_url = f"{settings.API_INT_URL}{settings.FUZZY_ENDPOINT}"

    def _preprocess_data(self, data, *args, **kwargs):
        try:
            gait_features = self.gait_features_extractor.extract_features(
                data["ACCELEROMETER"]["ACCELEROMETER_TIMES"],
                data["ACCELEROMETER"]["ACCELEROMETER_x"],
                data["ACCELEROMETER"]["ACCELEROMETER_y"],
                data["ACCELEROMETER"]["ACCELEROMETER_z"])
        except Exception as e:
            print(f"{e} exception while extracting features")
            return {"error": str(traceback.format_exc())}
        return gait_features

    def _process_data(self, data, *args, **kwargs):
        if "patient_id" not in kwargs:
            return {"error": "Patient id not passed down to fuzzy processor"}
        try:
            patient_id = kwargs["patient_id"]
            fuzzy_setup = self._download_fuzzy_setup(patient_id)
            user_score_system = self.fuzzy_logic_evaluator.create_system(fuzzy_setup)
            user_score = self.fuzzy_logic_evaluator.compute_user_score(user_score_system,
                                                                       data)
        except Exception:
            return {"error": str(traceback.format_exc())}
        return {"user_score": user_score}

    def _download_fuzzy_setup(self, patient_id):
        response = self.request_handler.send_request("GET",
                                                     f"{self._fuzzy_download_url}{patient_id}")

        return response.json()
