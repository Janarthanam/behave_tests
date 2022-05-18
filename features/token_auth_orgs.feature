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