"""
Created on Thu Nov 19 13:14:46 2020

@author: ars22

Refactored and included in the project by: jas103
"""
import numpy as np


class PeaksDetector:
    def __init__(self):
        pass

    def detect_peaks(self, data):
        threshold = np.mean(data) + 0.5 * np.std(data)

        peak_indexes = []

        peak = -np.inf

        # TODO: ask why -2?
        for index, possible_peak in enumerate(data[:-2], start=1):
            if possible_peak > peak:
                peak = possible_peak

                if peak > data[index] and peak > threshold:
                    peak_indexes.append(index)
            peak = possible_peak

        return peak_indexes
