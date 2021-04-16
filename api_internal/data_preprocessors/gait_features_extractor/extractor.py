from data_preprocessors.gait_features_extractor.gait_parameters_extractor import \
    GaitParametersExtractor
from data_preprocessors.gait_features_extractor.peaks_extractor import PeaksExtractor


class Extractor:
    def __init__(self):
        self.peaks_extractor = PeaksExtractor()
        self.gait_parameters_extractor = GaitParametersExtractor()

    def extract_features(self, times, accelerometer_x, accelerometer_y, accelerometer_z):
        limit_by = 18
        times, accelerometer_z = self._limit_to_seconds(limit_by, times, accelerometer_z)
        peaks = self.peaks_extractor.detect_peaks(times, accelerometer_x, accelerometer_y,
                                                  accelerometer_z)
        gait_parameters = self.gait_parameters_extractor.extract_features(peaks.heel_strike_times,
                                                                          peaks.toe_off_times)

        print(f"steps: {limit_by/gait_parameters.step_seconds}")
        return gait_parameters

    def _limit_to_seconds(self, no_of_seconds, times, acc_z):
        no_of_millis = no_of_seconds * 1000
        to = None
        for i, t in enumerate(times):
            if t >= no_of_millis:
                to = i
                break
        if to:
            return times[:to], acc_z[:to]
        print(times[-1])
        return times, acc_z
