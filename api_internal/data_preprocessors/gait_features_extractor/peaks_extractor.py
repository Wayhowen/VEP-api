"""
Created on Thu Jan  9 10:41:42 2020

@author: ars22

Refactored and included in the project by: jas103
"""

# read for understanding gaits variations
# (https://www.science.gov/topicpages/c/cadence+stride+length)

from detectors.heel_strike_detector import HeelStrikeDetector
# https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/48641/versions/1/previews/SCA/peakdet.m/index.html
from detectors.leading_leg_detector import LeadingLegDetector
from detectors.peaks_detector import \
    PeaksDetector  # it detects all the peaks where heel strike and toe-off occurs.
from detectors.toe_off_detector import ToeOffDetector
from dto.peak_extraction_result import PeakExtractionResult
from filters.butterworth import \
    ButterworthCalculator  # Preprocessing using frequency information from FFT
from filters.fft import FFTCalculator  # Fourier transform


class PeaksExtractor:
    def __init__(self):
        self.fft_calculator = FFTCalculator()
        self.butterworth_calculator = ButterworthCalculator()
        self.peaks_detector = PeaksDetector()
        self.heel_strike_detector = HeelStrikeDetector()
        self.toe_off_detector = ToeOffDetector()
        self.leading_leg_detector = LeadingLegDetector()

        self.sampling_rate = None

    # z in here is used as forward axis, y - horizontal, x - vertical
    def detect_peaks(self, times, accelerometer_x, accelerometer_y, accelerometer_z) \
            -> PeakExtractionResult:
        self._calculate_sampling_rate(times, accelerometer_z)

        filtered_z = self._filter_data(accelerometer_z, times)

        # Detect peaks from vertical (X_axis) and forward acceleration (Z_axis)

        # Z Axis peaks
        peak_indexes_z = self.peaks_detector.detect_peaks(filtered_z)

        # true peaks = max peaks = toe-off
        toe_off_indexes = self.toe_off_detector.detect_toe_offs(times, filtered_z, peak_indexes_z,
                                                                self.sampling_rate)

        # TODO: We need to detect beginning and ending of the signal automatically, maybe by stdev

        # min peaks = heel-strike
        heel_strike_indexes = self.heel_strike_detector.detect_heel_strikes(filtered_z,
                                                                            toe_off_indexes)

        toe_off_times = [(times[toe_off_index] / 1000) for toe_off_index in toe_off_indexes]
        heel_strike_times = [(times[heel_strike_index] / 1000) for heel_strike_index in
                             heel_strike_indexes]

        detected_peaks = PeakExtractionResult(toe_off_times, heel_strike_times)
        return detected_peaks

    # pylint:disable=unused-variable
    def _filter_data(self, accelerometer_z, times):
        # Apply Butterworth zerolag filter (filtfilt) Transform on channel Z, as it should be more
        # reliable (if phone positioned correctly)

        # TODO: change depending on the activity
        accelerometer_z = self.butterworth_calculator.smooth_data(accelerometer_z,
                                                                  self.sampling_rate)

        #  Apply Fourier Transform on the channel Z, as all channels give the same dominant
        #  frequency, so we use just the forward one.

        peak_indexes_z, peak_frequencies_z = self.fft_calculator.calculate_fft(accelerometer_z,
                                                                               self.sampling_rate)

        return accelerometer_z

    def _calculate_sampling_rate(self, times, accelerometer_z):
        self.sampling_rate = len(accelerometer_z) / times[-1] * 1000
