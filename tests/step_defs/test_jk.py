from pytest_bdd import scenario, given, when, then, scenarios, parsers

scenarios('../features/jk.feature')


@scenario(feature_name="jk.feature", scenario_name="Outlined_01", features_base_dir="../features")
def Outlined_01():
    pass


@given(parsers.parse('{user01} go to beijin'))
def step_given(user01):
    print("\r\n")
    print(user01)
    assert user01 == "github1983"


@when(parsers.parse("{user02} go to shanghai"))
def step_when(user02):
    print(u'STEP: When  "<user>" steps')
    assert user02 == "github1983"


@then(parsers.parse("the basket contains {total} cucumbers"))
def step_then(total):
    if isinstance(total, str):
        print(type(total))

    assert total == "2"
