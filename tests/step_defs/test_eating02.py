# from pytest_bdd import scenarios, given, parsers, when, then, scenario
#
# scenarios('../features/eating02.feature')
#
#
# @scenario(feature_name="eating02.feature", scenario_name="Outlined_02", features_base_dir="../features")
# def Outlined_02():
#     pass
#
#
# @given(parsers.parse("there are {start:d} cucumbers02"), target_fixture="cucumbers")
# def given_cucumbers(start):
#     return {"start": start, "eat": 0}
#
#
# @when(parsers.parse("I eat {eat:d} cucumbers02"))
# def eat_cucumbers(cucumbers, eat):
#     cucumbers["eat"] += eat
#
#
# @then(parsers.parse("I should have {left:d} cucumbers02"))
# def should_have_left_cucumbers(cucumbers, left):
#     assert cucumbers["start"] - cucumbers["eat"] == left