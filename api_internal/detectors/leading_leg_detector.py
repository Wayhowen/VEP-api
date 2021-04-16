"""
Created on Mon Apr  5 21:06:29 2021

@author: ars22

Refactored and included in the project by: jas103
"""


class LeadingLegDetector:
    def __init__(self):
        pass

    # ---------------------------
    # Left or Right leg identification
    # ---------------------------
    def detect_legs(self, accelerometer_z, toe_off_indexes):
        right_leg_indexes, left_leg_indexes = set(), set()

        if self._leading_leg(accelerometer_z, toe_off_indexes) == "L":
            for index, peak in enumerate(toe_off_indexes):
                if index % 2 == 0:
                    left_leg_indexes.add(peak)

                else:
                    right_leg_indexes.add(peak)

        else:
            for index, peak in enumerate(toe_off_indexes):
                if index % 2 == 0:
                    right_leg_indexes.add(peak)
                else:
                    left_leg_indexes.add(peak)

        return right_leg_indexes, left_leg_indexes

    def _leading_leg(self, accelerometer_z, toe_off_indexes):
        if accelerometer_z[toe_off_indexes[0]] <= 0:
            # From videos, if amplitude is <0, left
            # we stopped at first index, as it is alternative later on.
            leading_leg = 'L'
        else:
            # actually its right leg, but false peak led us do that
            leading_leg = 'R'
        return leading_leg
