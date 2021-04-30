"""
Created on Thu Nov 19 14:39:54 2020

@author: ars22

Refactored and included in the project by: jas103
"""
import scipy.signal as signal


class ButterworthCalculator:
    def __init__(self):
        self.cutoff_frequency = 6  # 10 is cut off frequency // might use 8

    # more noisy signal - smaller filtering frequency/ less noisy - up to 10
    def smooth_data(self, data, sampling_rate):
        nyquist = sampling_rate * 0.5  # nyquist principle half of the frequencies pass

        filter_frequency = self.cutoff_frequency / nyquist

        # can check with 3 or 4 how it works
        n = 2  # filtering order

        data = signal.detrend(data)  # Removing mean from the signal before applying filter

        b, a = signal.butter(n, filter_frequency, btype='low', output='ba')

        smooth_data = signal.filtfilt(b, a, data)  # zero phase delay filter

        return smooth_data
