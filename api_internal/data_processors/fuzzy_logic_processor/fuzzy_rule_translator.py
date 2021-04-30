import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyRuleTranslator:
    def __init__(self, universe_dict=None):
        self._universe = universe_dict
        self._operators = {
            "and": "&",
            "or": "|",
        }

    def set_universe(self, universe):
        self._universe = universe

    def from_text_to_fuzzy_logic(self, rules_texts_list):
        assert self._universe is not None, "Call `set_universe` method first"
        fuzzy_logic_rules = []
        for rule_text in rules_texts_list:
            rule = ctrl.Rule()

            rule_text = self._sanitize_text(rule_text)

            antecedent_text, consequent_text = rule_text.split("then")

            rule.consequent = self._get_consequent(consequent_text)
            rule.antecedent = self._get_antecedent(antecedent_text)

            fuzzy_logic_rules.append(rule)

        return fuzzy_logic_rules

    def from_fuzzy_logic_to_text(self, logic_list):
        raise NotImplementedError

    def _sanitize_text(self, rule_text):
        rule_text = rule_text.lower()
        rule_text = rule_text.replace("if ", "")
        rule_text = rule_text.replace("is", "")
        rule_text = rule_text.replace("are", "")
        return rule_text

    def _get_consequent(self, consequent_text):
        splitted_consequent = consequent_text.split()
        consequent_fuzzy = self._universe[splitted_consequent[0]][splitted_consequent[1]]
        return consequent_fuzzy

    def _get_antecedent(self, antecedent_text):
        splitted_antecedent = antecedent_text.split()
        final_rule = ""
        while splitted_antecedent:
            universe, membership, *splitted_antecedent = splitted_antecedent
            if membership == "not":
                negation = "~ "
                membership = splitted_antecedent.pop(0)
                condition = f"{negation} self._universe['{universe}']['{membership}'] "
            else:
                condition = f"self._universe['{universe}']['{membership}'] "
            final_rule += condition
            if splitted_antecedent:
                clause = self._operators[splitted_antecedent.pop(0)]
                final_rule += f"{clause} "
        return eval(final_rule)


if __name__ == "__main__":
    univ = {}
    tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')
    tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
    tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
    tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

    quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
    quality.automf(5)
    service.automf(3)

    univ["tip"] = tip
    univ["quality"] = quality
    univ["service"] = service

    frt = FuzzyRuleTranslator(univ)
    rules = frt.from_text_to_fuzzy_logic(["If quality is not poor and service is good or service"
                                          " is average then tip is high"])
