class PeakExtractionResult:
    def __init__(self, toe_off_times, heel_strike_times):
        self.toe_off_times = toe_off_times
        self.heel_strike_times = heel_strike_times

    def __str__(self):
        return (f"Toe off times: {self.toe_off_times}\n"
                f"Heel strike times: {self.heel_strike_times}\n")
