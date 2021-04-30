"""
Created on Fri Jan 17 11:50:04 2020

@author: ars22

Refactored and included in the project by: jas103
"""
from scipy import fftpack
import numpy as np


class FFTCalculator:
    def __init__(self):
        pass

    def calculate_fft(self, data, sr):
        data_points = len(data)

        sample_spacing = 1 / sr

        # Frequencies of the data set to be deployed at the x-axis
        frequencies = np.linspace(0.0, 1.0 / (2.0 * sample_spacing), data_points // 2)

        # calculating fft using scipy library of python
        fft_data = fftpack.fft(data)

        # get the indices with the max value
        peak_indexes = np.argmax(2.0 / data_points * np.abs(fft_data[:data_points // 2])[:], axis=0)

        # now use the indices to get the corresponding frequencies
        peak_frequencies = frequencies[peak_indexes]

        # peak frequency is the most important
        return peak_indexes, peak_frequencies
