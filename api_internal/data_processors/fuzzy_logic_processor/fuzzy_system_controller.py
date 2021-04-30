from skfuzzy import control

from data_processors.fuzzy_logic_processor.fuzzy_rule_translator import FuzzyRuleTranslator
from data_processors.fuzzy_logic_processor.fuzzy_universe_creator import FuzzyUniverseCreator


class FuzzySystemController:
    def __init__(self):
        self.universe_creator = FuzzyUniverseCreator()
        self.rule_translator = FuzzyRuleTranslator()

        self.universe_descriptions = None
        self.fuzzy_rules = None

    def create_system(self, fuzzy_setup):
        self.universe_descriptions = fuzzy_setup["universes_description"]
        self.fuzzy_rules = fuzzy_setup["rules"]

        universe = self.universe_creator.create_fuzzy_universes(self.universe_descriptions)
        self.rule_translator.set_universe(universe)
        rules = self.rule_translator.from_text_to_fuzzy_logic(self.fuzzy_rules)

        evaluation_control = control.ControlSystem(rules)
        user_score_system = control.ControlSystemSimulation(evaluation_control,
                                                            cache=False, clip_to_bounds=True,
                                                            flush_after_run=1)

        return user_score_system

    def compute_user_score(self, user_score_system, features):
        for feature_name, feature_value in features.items():
            if feature_name in self.universe_descriptions:
                user_score_system.input[feature_name] = feature_value
        user_score_system.compute()
        user_score = user_score_system.output["user_score"]
        return user_score
