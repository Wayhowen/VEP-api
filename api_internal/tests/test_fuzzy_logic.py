import unittest

import numpy
import numpy as np
import skfuzzy.control
from skfuzzy import control, trimf

from data_processors.fuzzy_logic_processor.fuzzy_system_controller import FuzzySystemController

UNIVERSES = {
    "quality": {
        "range": (0, 11, 1),
        "membership_functions": [
            {
                "default": 5
            }
        ]
    },
    "service": {
        "range": (0, 11, 1),
        "membership_functions": [
            {
                "default": 3
            }
        ]
    },
}

RULES = [
    "If quality is poor or service is poor then user_score is bad",
    "If service is average then user_score is average",
    "If service is good or quality is good then user_score is good"
]


class TestFuzzyLogic(unittest.TestCase):
    def test_system_controller_creates_system_sucessfully(self):
        """
        Try to create a system controller from a set of rules and universe description and check if
        the system is indeed created
        """
        fuzzy_setup = {"universes_description": UNIVERSES,
                       "rules": RULES}
        system_controller = FuzzySystemController()
        user_score_system = system_controller.create_system(fuzzy_setup)
        self.assertEqual(type(user_score_system),
                         skfuzzy.control.controlsystem.ControlSystemSimulation)

    def test_fuzzy_system_can_compute_score(self):
        """
        Try to compute a fuzzy system output and see if the system can compute it and if the output
        is numeric
        """
        fuzzy_setup = {"universes_description": UNIVERSES,
                       "rules": RULES}
        system_controller = FuzzySystemController()
        user_score_system = system_controller.create_system(fuzzy_setup)
        user_score_system.input['quality'] = 6.5
        user_score_system.input['service'] = 9.8
        user_score_system.compute()
        self.assertIsNotNone(user_score_system.output['user_score'])
        self.assertEqual(type(user_score_system.output["user_score"]),
                         numpy.float64)

    def test_fuzzy_system_produces_same_output_as_example(self):
        """
        Try to compute a fuzzy system output and compare it against an output produced by a system
        created manually by the creators of the skfuzzy library
        https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html#example-plot-tipping-problem-newapi-py
        """
        fuzzy_setup = {"universes_description": UNIVERSES,
                       "rules": RULES}
        system_controller = FuzzySystemController()
        user_score_system = system_controller.create_system(fuzzy_setup)
        user_score_system.input['quality'] = 6.5
        user_score_system.input['service'] = 9.8
        user_score_system.compute()
        manually_created_score = self._get_score_from_manually_created_universe()
        self.assertEqual(user_score_system.output["user_score"], manually_created_score)

    def _get_score_from_manually_created_universe(self):
        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        quality = control.Antecedent(np.arange(0, 11, 1), 'quality')
        service = control.Antecedent(np.arange(0, 11, 1), 'service')
        tip = control.Consequent(np.arange(-1, 2, 1), 'tip')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        quality.automf(5)
        service.automf(3)

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tip['bad'] = trimf(tip.universe, [-1, -1, 0])
        tip['average'] = trimf(tip.universe, [-0.5, 0, 0.5])
        tip['good'] = trimf(tip.universe, [0, 1, 1])

        rule1 = control.Rule(quality['poor'] | service['poor'], tip['bad'])
        rule2 = control.Rule(service['average'], tip['average'])
        rule3 = control.Rule(service['good'] | quality['good'], tip['good'])

        tipping_ctrl = control.ControlSystem([rule1, rule2, rule3])

        tipping = control.ControlSystemSimulation(tipping_ctrl)

        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        tipping.input['quality'] = 6.5
        tipping.input['service'] = 9.8

        # Crunch the numbers
        tipping.compute()
        return tipping.output['tip']

    def test_fuzzy_system_can_work_on_problem_from_gait_domain(self):
        """
        Check if a system is capable of creating other universes and functions and then using that
        system to assess different inputs.
        """
        fuzzy_setup = {"universes_description": {"step_asymmetry_seconds": {
            "range": (0, 0.31, 0.01),
            "membership_functions": [
                {
                    "label": "normal",
                    "type": "triangle",  # might be trapezoid
                    "points": [0, 0, 0.02]
                },
                {
                    "label": "abnormal",
                    "type": "triangle",  # might be trapezoid
                    "points": [0.01, 0.04, 0.10]
                },
                {
                    "label": "bad",
                    "type": "trapezoid",  # might be trapezoid
                    "points": [0.08, 0.12, 0.31, 0.31]  # if trapezoid - 4 points required
                },
            ]
        }},
            "rules": ["If step_asymmetry_seconds are normal then user_score is good",
                      "If step_asymmetry_seconds are abnormal then user_score is average",
                      "If step_asymmetry_seconds are bad then user_score is bad", ]}
        system_controller = FuzzySystemController()
        user_score_system = system_controller.create_system(fuzzy_setup)
        user_score_system.input['step_asymmetry_seconds'] = 0.01
        user_score_system.compute()
        self.assertAlmostEqual(user_score_system.output["user_score"], 0.6111111111111112, 3)
        user_score_system.input['step_asymmetry_seconds'] = 0.07
        user_score_system.compute()
        self.assertAlmostEqual(user_score_system.output["user_score"], 0.0, 3)
        user_score_system.input['step_asymmetry_seconds'] = 0.15
        user_score_system.compute()
        self.assertAlmostEqual(user_score_system.output["user_score"], -0.6666666666666667, 3)
