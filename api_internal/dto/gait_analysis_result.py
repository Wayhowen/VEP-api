class GaitAnalysisResult:
    def __init__(self, step_seconds, left_step_seconds, right_step_seconds, stride_seconds,
                 stance_seconds, swing_seconds, step_asymmetry_seconds, step_fluctuation_seconds,
                 stance_percentage, swing_percentage, double_support_percentage):
        self.step_seconds = step_seconds
        self.left_step_seconds = left_step_seconds
        self.right_step_seconds = right_step_seconds
        self.stride_seconds = stride_seconds
        self.stance_seconds = stance_seconds
        self.swing_seconds = swing_seconds
        self.step_asymmetry_seconds = step_asymmetry_seconds
        self.step_fluctuation_seconds = step_fluctuation_seconds
        self.stance_percentage = stance_percentage
        self.swing_percentage = swing_percentage
        self.double_support_percentage = double_support_percentage

    def __repr__(self):
        return f"{vars(self)}"

    def as_json(self):
        return vars(self)

    def as_dict(self):
        return vars(self)
