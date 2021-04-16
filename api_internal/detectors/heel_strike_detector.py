"""
Created on Sat Dec  5 21:08:50 2020

@author: ars22

Refactored and included in the project by: jas103
"""


class HeelStrikeDetector:
    def __init__(self):
        pass

    def detect_heel_strikes(self, data, peaks):
        heel_strikes = []

        if type(data) is not list and len(data) != 0:
            data = data.tolist()

        for index, peak in enumerate(peaks[1:]):
            heel_strike = min(data[peaks[index]:peak])

            heel_strike_indexes = data.index(heel_strike)

            heel_strikes.append(heel_strike_indexes)

        return heel_strikes
