import numpy as np
from skfuzzy import control, trapmf, trimf


class FuzzyUniverseCreator:
    def __init__(self):
        pass

    def create_fuzzy_universes(self, universes_description):
        universes = self._create_universes_from_description(universes_description)
        universes["user_score"] = self._create_user_score()
        return universes

    def _create_universes_from_description(self, universes_description):
        universes = {}
        for name, details in universes_description.items():
            universe = control.Antecedent(np.arange(*details["range"]), name)
            if len(details["membership_functions"]) == 1 and \
                    "default" in details["membership_functions"][0]:
                universe.automf(details["membership_functions"][0]["default"])
            else:
                for function in details["membership_functions"]:
                    label = function["label"]
                    function_type = function["type"]
                    points = function["points"]
                    if function_type == "triangle":
                        universe[label] = trimf(universe.universe, points)
                    elif function_type == "trapezoid":
                        universe[label] = trapmf(universe.universe, points)
            universes[name] = universe
        return universes

    def _create_user_score(self):
        user_score = control.Consequent(np.arange(-1, 2, 1), 'user_score')
        user_score['bad'] = trimf(user_score.universe, [-1, -1, 0])
        user_score['average'] = trimf(user_score.universe, [-0.5, 0, 0.5])
        user_score['good'] = trimf(user_score.universe, [0, 1, 1])
        return user_score
