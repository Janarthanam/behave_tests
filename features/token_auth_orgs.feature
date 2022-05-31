Feature: token orgs

Scenario: generate a token for an org
    Given I am a tenant admin
    When The tenant has 1 orgs
    Then I get an user token for "tsadmin" using secret in org 1
    When I try to login using that token in to "tsadmin"
    Then I should be logged in to org 1

Scenario: generate a token for an org
    Given I am a tenant admin
    When The tenant has 2 orgs
    Then I get an user token for "tsadmin" using secret in org 1
    When I try to login using that token in to "tsadmin"
    Then I should be logged in to org 2

#todo
Scenario Outline: generate token for user in various states
    Given I am a tenant admin
    When I add an user
    Then I change user above to state "<state>"
    When I update the user above
    Then I get an user token for above using secret
    Then I get an error <code>
    Examples: state
        |   state | code |
        | INACTIVE| 403 |
        | LOCKED  | 403 |
        | EXPIRED | 403 |
        | ACTIVE  | 200 |