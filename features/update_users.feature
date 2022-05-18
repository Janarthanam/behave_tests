Feature: Update user

Scenario: Update user removes org
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When Update the user to add orgs
        | orgs |
        | 2    |   
    Then the user belongs to
        | orgs |
        | 2    |
    When I try to remove the user from group for org 2
    Then I get an error 400

Scenario: Update user api can add and remove user org association
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When Update the user to add orgs
        |orgs|
        | 1 |
        | 2 |
    Given I am an org admin for org 1
    Then remove the user from org 1
    Then the user belongs to
        | orgs |
        | 1    |



