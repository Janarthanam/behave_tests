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
        | 1    |
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

Scenario: Even tenant admin cant remove user from an org by removing from org group
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When I try to remove the user from group for org 1
    Then the user belongs to group
        | orgs |
        | 1    |
    #Then I get an error 400


Scenario: Update user removes groups in that org
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
    When Adding an user to org 1
    Then I add the user above to the group above
    Then the user belongs to
        | orgs |
        | 1    |
    Then the user belongs to group
        | groups | orgs |
        | "above"| 1    |

Scenario: Create user in org as org admin
  Given I am a tenant admin
  When The tenant has 2 orgs
  Then I add a group to the org 1
  Given I switch to org 1
  When Adding an user to org 1
  Then I add the user above to the group above  
  Then the user belongs to
      | orgs |
      | 1    |
  Then the user belongs to group
    | groups | orgs |
    | "above" | 1   |

Scenario: Org admin only sees her org groups
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    Then I add a group to the org 1
    Then I add the user above to the group above
    Then the user belongs to group
        | groups | orgs |
        | "above"| 1    |
    When Update the user to modify orgs
        |orgs|
        | 1 |
        | 2 |
    When I get the user above
    Then the user belongs to group
        | groups | orgs |
        | "above"| 1    |
        | "above" | 2   |
    When I get the user above
    Then the user belongs to
        | orgs |
        | 1    |
        | 2    |
    Given I am an org admin for org 1
    #fetch the user again for org view
    When I get the user above
    Then the user belongs to group
        | groups | orgs |
        | "above"| 1    |

#mixed org
#org admin
Scenario: Update user api can only be used add groups for org admin.
    Given I am a tenant admin
    When The tenant has 2 orgs
    When Adding an user to org 1
    When Update the user to modify orgs
        |orgs|
        | 1 |
        | 2 |
    When I get the user above
    Then the user belongs to group
        | orgs |
        | 1    |
        | 2    |
    Then I add a group to the org 1
    Given I am an org admin for org 1
    #fetch the user again for org view
    When I get the user above
    When I update the user above to add group above
    Then the user belongs to group
        | groups | orgs |
        | "above" | 1     |
    Given I am a tenant admin
    When I get the user above
    Then the user belongs to group
        | orgs |groups|
        | 1    | "above"|
        | 2    | "above" |
    