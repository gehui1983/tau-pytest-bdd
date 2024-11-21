# Created by gehui at 2024/11/1
Feature: # Enter feature name here
  # Enter feature description here
    Scenario Outline: Outlined_02
        Given there are <start> cucumbers02
        When I eat <eat> cucumbers02
        Then I should have <left> cucumbers02

        Examples:
        | start | eat | left |
        |  12   |  5  |  7   |
        |  12   |  7  |  5   |
        |  20   |  5  |  15  |