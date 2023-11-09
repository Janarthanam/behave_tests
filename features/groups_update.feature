Feature: Group updates

Scenario: Group update to a different org group
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When I add the user to an org 2 group
    Then I get an error 400
