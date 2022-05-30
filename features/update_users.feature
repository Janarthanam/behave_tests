Feature: Update user

Scenario: Update user removes org
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When Update the user to modify orgs
        | orgs |
        | 1    |
        | 2    |
    Then the user belongs to group
        | orgs |
        | 1    
        | 2    |
    When Update the user to modify orgs
        | orgs |
        | 2    |
    Then the user belongs to
        | orgs |
        | 2    |
    Then the user belongs to group
        | orgs |
        | 2    |
    When I try to remove the user from group for org 2
    Then the user belongs to group
        | orgs |
        | 2    |
    Then I get an error 400


Scenario: Update user removes groups in org
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    Then I add a group to the org 1
    Then I add the user above to the group above
    Then the user belongs to
        | orgs |
        | 1    |
    Then the user belongs to group
        | groups | orgs |
        | "above"| 1    |
    When Update the user to modify orgs
        | orgs |
        | 2    |
    Then the user belongs to
        | orgs |
        | 2    |
    Then the user belongs to group
        | orgs |
        | 2    |

Scenario: Create user in org retains groups and orgs correctly
    Given I am a tenant admin
    When The tenant has 2 orgs
    Then I add a group to the org 1
    When Adding an user to the org 1 and group above
    Then the user belongs to
        | orgs |
        | 1    |
    Then the user belongs to group
        | groups | orgs |
        | "above"| 1    |


Scenario: Create user in org as org admin
  Given I am a tenant admin
  When The tenant has 2 orgs
  Given I switch to org 1
  Then I add a group to the org 1
  When Adding an user to org 1 and group above
  Then the user belongs to
      | orgs |
      | 1    |
  Then the user belongs to group
    | groups | orgs |
    | "above" | 1   |




Scenario: Update user api can add and remove user org association
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When Update the user to modify orgs
        |orgs|
        | 1 |
        | 2 |
    Given I am an org admin for org 1
    Then remove the user from org 1
    Then I get an error 403
