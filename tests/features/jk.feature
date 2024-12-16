# Created by james at 12/14/24
Feature: Enter feature name here
  # Enter feature description here

    Scenario Outline: Outlined_01
    # Enter steps here
        Given <user01> go to beijin
        When  <user02> go to shanghai
        Then the basket contains <total> cucumbers

        Examples:
        | user01   | user02   | total |
        |github1983|github1983|2      |
        |github1983|github1983|2      |
        |github1983|github1983|2      |
