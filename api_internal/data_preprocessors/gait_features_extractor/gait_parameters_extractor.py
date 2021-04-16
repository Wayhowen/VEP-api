"""
Created on Wed Dec  9 16:49:02 2020

@author: ars22

Refactored and included in the project by: jas103
"""

import numpy as np

from dto.gait_analysis_result import GaitAnalysisResult


class GaitParametersExtractor:
    def __init__(self):
        self.step_times = []
        self.left_step_times = []
        self.right_step_times = []
        self.stride_times = []
        self.stance_times = []
        self.stance_ratios = []
        self.swing_times = []
        self.swing_ratios = []
        self.double_support_times = []
        self.asymmetries = []
        self.fluctuations = []

    def extract_features(self, heel_strikes, toe_offs):

        # not an output, just for better understaidng of each subject assymetry
        self.left_step_times, self.right_step_times, \
            self.step_times = self._extract_step_times(toe_offs)

        self.asymmetries = self._extract_asymmetries(self.right_step_times, self.left_step_times)

        self.fluctuations = self._calculate_fluctuation(self.left_step_times, self.right_step_times)

        for index, (toe_off, heel_strike) in enumerate(list(zip(toe_offs, heel_strikes))[2:],
                                                       start=2):
            stride = self._extract_common_properties(toe_off, toe_offs, heel_strike, index)

            # right leg supposedly
            if index % 2 == 0:
                if heel_strike > toe_off:
                    # possibly left or right, not necessary
                    double_support_time_1 = heel_strike - toe_off
                    double_support_time_2 = heel_strikes[index - 2] - toe_offs[index - 2]
                    double_support_time = double_support_time_1 + double_support_time_2
                    double_support_ratio = (double_support_time / stride)

                    self.double_support_times.append(double_support_ratio)

            # left leg supposedly
            elif index % 2 == 1:
                if heel_strike > toe_off:
                    double_support_time_1 = toe_off - heel_strikes[index - 1]
                    double_support_time_2 = toe_offs[index - 1] - heel_strikes[index - 2]
                    double_support_time = double_support_time_1 + double_support_time_2
                    double_support_ratio = (double_support_time / stride)

                    self.double_support_times.append(double_support_ratio)

        raw_analysis_result = {
            'step_seconds': float(
                "{:.2f}".format(np.mean(np.asarray(self.step_times).astype(float)))),
            'left_step_seconds': float(
                "{:.2f}".format(np.mean(np.asarray(self.left_step_times).astype(float)))),
            'right_step_seconds': float(
                "{:.2f}".format(np.mean(np.asarray(self.right_step_times).astype(float)))),
            'stride_seconds': float(
                "{:.2f}".format(np.mean(np.asarray(self.stride_times).astype(float)))),
            'stance_seconds': float(
                "{:.2f}".format(np.mean(np.asarray(self.stance_times).astype(float)))),
            'stance_percentage': float(
                "{:.2f}".format(np.mean(np.asarray(self.stance_ratios).astype(float)))),
            'swing_seconds': float(
                "{:.2f}".format(np.mean(np.asarray(self.swing_times).astype(float)))),
            'swing_percentage': float(
                "{:.2f}".format(np.mean(np.asarray(self.swing_ratios).astype(float)))),
            'double_support_percentage': float(
                "{:.2f}".format(np.mean(np.asarray(self.double_support_times).astype(float)))),
            'step_asymmetry_seconds': float(
                "{:.3f}".format(np.mean(np.asarray(self.asymmetries).astype(float)))),
            'step_fluctuation_seconds': float(
                "{:.3f}".format(np.mean(np.asarray(self.fluctuations).astype(float))))

        }
        analysis_result = GaitAnalysisResult(**raw_analysis_result)
        return analysis_result

    def _extract_common_properties(self, toe_off, toe_offs, heel_strike, index):
        stride = toe_off - toe_offs[index - 2]
        self.stride_times.append(stride)

        swing_time, swing_ratio = self._calculate_swing_time_and_ratio(heel_strike,
                                                                       toe_off,
                                                                       stride)
        self.swing_times.append("{:.2f}".format(swing_time))
        self.swing_ratios.append("{:.2f}".format(swing_ratio))

        stance_time, stance_ratio = self._calculate_stance_time_and_ratio(swing_time,
                                                                          stride)
        self.stance_times.append("{:.2f}".format(stance_time))
        self.stance_ratios.append("{:.2f}".format(stance_ratio))
        return stride

    def _extract_step_times(self, toe_offs):
        # not an output, just for better understanding of each subject asymmetry
        left_step_times, right_step_times, step_times = [], [], []

        for index, toe_off in enumerate(toe_offs[1:], start=1):
            if index % 2 == 0:
                right_step_time = toe_off - toe_offs[index - 1]
                right_step_times.append(right_step_time)
                step_times.append(right_step_time)

            elif index % 2 == 1:
                left_step_time = toe_off - toe_offs[index - 1]
                left_step_times.append(left_step_time)
                step_times.append(left_step_time)

        return left_step_times, right_step_times, step_times

    def _extract_asymmetries(self, right_step_times, left_step_times):
        asymmetries = []
        for right_step_time, left_step_time in zip(right_step_times, left_step_times):
            asymmetry = abs((right_step_time - left_step_time) / (right_step_time + left_step_time))
            asymmetries.append(asymmetry)
        return asymmetries

    def _calculate_fluctuation(self, array1, array2):
        fluctuation_1 = np.var(array1)
        fluctuation_2 = np.var(array2)
        resulting_fluctuation = (fluctuation_1 + fluctuation_2) / 2
        return [resulting_fluctuation]

    def _calculate_swing_time_and_ratio(self, heel_strike, toe_off, stride):
        swing_time = heel_strike - toe_off
        swing_ratio = swing_time / stride
        return swing_time, swing_ratio

    def _calculate_stance_time_and_ratio(self, swing_time, stride):
        stance_time = stride - swing_time
        stance_ratio = stance_time / stride
        return stance_time, stance_ratio
