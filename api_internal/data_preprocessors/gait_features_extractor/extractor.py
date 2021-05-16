from data_preprocessors.gait_features_extractor.gait_parameters_extractor import \
    GaitParametersExtractor
from data_preprocessors.gait_features_extractor.peaks_extractor import PeaksExtractor


class Extractor:
    def __init__(self):
        self.peaks_extractor = PeaksExtractor()
        self.gait_parameters_extractor = GaitParametersExtractor()

    def extract_features(self, times, accelerometer_x, accelerometer_y, accelerometer_z):
        peaks = self.peaks_extractor.detect_peaks(times, accelerometer_x, accelerometer_y,
                                                  accelerometer_z)
        gait_parameters = self.gait_parameters_extractor.extract_features(peaks.heel_strike_times,
                                                                          peaks.toe_off_times)

        return gait_parameters
