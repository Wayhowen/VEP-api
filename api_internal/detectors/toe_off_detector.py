"""
Created on Sun Nov 29 11:51:49 2020

@author: ars22

Refactored and included in the project by: jas103
"""


class ToeOffDetector:
    def __init__(self):
        self.walk_adjustment = 0.5

    def detect_toe_offs(self, time, data, max_peaks_indexes, sampling_rate):
        # TODO: need to update it later on to make it adaptive

        # 0.5 is constant to adjust change in walk and 1000 is to convert in milliseconds
        threshold = time[int(sampling_rate / 3)]

        # Sometime data is colletced as numpy array, however, to get index, we need data in list
        # format
        data = list(data)

        toe_offs = []

        current_peak = max_peaks_indexes[0]

        for index, peak in enumerate(max_peaks_indexes[:-1]):
            if time[current_peak] < time[peak] and (time[peak] - time[current_peak]) < threshold:
                current_peak = data.index(max(data[peak], data[current_peak]))

                if (time[max_peaks_indexes[index + 1]] - time[current_peak]) > threshold:
                    toe_offs.append(current_peak)
                    current_peak = max_peaks_indexes[index + 1]

            elif (time[peak] - time[current_peak]) >= threshold:
                toe_offs.append(current_peak)
                current_peak = peak

        return toe_offs
