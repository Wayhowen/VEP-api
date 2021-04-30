from rest_framework import serializers


class FuzzyValidator:
    def __init__(self):
        pass

    # TODO: Add validation by regex
    def validate_rules(self, data):
        if isinstance(data, list):
            if len(data) >= 2:
                for entry in data:
                    if not isinstance(entry, str):
                        raise serializers.ValidationError("All list entries must be of type string")
                return data
            raise serializers.ValidationError("There must be at least 2 rules")
        raise serializers.ValidationError("Rules must be a list")

    def validate_patient(self, data):
        if data is None:
            raise serializers.ValidationError("The patient cannot be null")
        return data

    def validate_universes(self, data):
        self._check_overall_structure(data)
        for universe_name, universe_description in data.items():
            self._check_range_property(universe_name, universe_description)
            self._check_membership_functions(universe_description, universe_name)

    def _check_overall_structure(self, data):
        if data is None:
            raise serializers.ValidationError("Universes description cannot be null")
        if not isinstance(data, dict):
            raise serializers.ValidationError("Universes description must be a dictionary")
        if len(data) < 1:
            raise serializers.ValidationError("There must be at least one universe declared")

    def _check_range_property(self, universe_name, universe_description):
        if "range" not in universe_description:
            raise serializers.ValidationError(
                f"Universe {universe_name} needs to have a range property")
        if not isinstance(universe_description["range"], list):
            raise serializers.ValidationError("Range property needs to be a list")
        if len(universe_description["range"]) != 3:
            raise serializers.ValidationError("Range property  must contain exactly 3 elements")
        for element in universe_description["range"]:
            if not isinstance(element, int) and not isinstance(element, float):
                raise serializers.ValidationError("Range property can contain only numbers")

    def _check_membership_functions(self, universe_description, universe_name):
        if "membership_functions" not in universe_description:
            raise serializers.ValidationError(f"Universe {universe_name} needs to have a "
                                              f"membership_functions property")
        if not isinstance(universe_description["membership_functions"], list):
            raise serializers.ValidationError("membership_functions property must be a list")
        if len(universe_description["membership_functions"]) < 1:
            raise serializers.ValidationError(
                "membership_functions property must either have default value or function "
                "description")
        for function in universe_description["membership_functions"]:
            self._check_default_and_custom(function)

    def _check_default_and_custom(self, function):
        if "default" in function:
            if function["default"] not in [3, 5, 7]:
                raise serializers.ValidationError(
                    "Membership functions default value must be either 3, 5 or 7")
        else:
            self._check_label(function)
            self._check_type(function)
            self._check_points(function)

    def _check_label(self, function):
        if "label" not in function:
            raise serializers.ValidationError(
                "Label property must be present for custom membership function")
        if not isinstance(function["label"], str):
            raise serializers.ValidationError("Label must be a string instance")

    def _check_type(self, function):
        if "type" not in function:
            raise serializers.ValidationError(
                "Type property must be present for custom membership function")
        if function["type"] not in ["triangle", "trapezoid"]:
            raise serializers.ValidationError(
                "Type property must be either a triangle or trapezoid")

    def _check_points(self, function):
        if "points" not in function:
            raise serializers.ValidationError(
                "Points property must be present for custom membership function")
        if not isinstance(function["points"], list):
            raise serializers.ValidationError("Points property must be a list")
        if len(function["points"]) != 3 and \
                function["type"] == "triangle":
            raise serializers.ValidationError("Points property must have length 3 for triangle")
        if len(function["points"]) != 4 and \
                function["type"] == "trapezoid":
            raise serializers.ValidationError("Points property must have length 4 for trapezoid")
        for point in function["points"]:
            if not isinstance(point, int) and not isinstance(point, float):
                raise serializers.ValidationError("Each point in a list must be a numeric")
