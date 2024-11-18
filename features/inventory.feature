Feature: The inventory store service back-end
    As a Inventory Manager
    I need a RESTful catalog service
    So that I can keep track of all my inventories

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Inventory
    When I visit the "Home Page"
    And I set the "Name" to "Milk"
    And I set the "Quantity" to "100"
    And I set the "Restock Level" to "10"
    And I select "Open_box" in the "Condition" dropdown
    And I select "True" in the "Restocking Available" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Milk" in the "Name" field
    And I should see "100" in the "Quantity" field
    And I should see "10" in the "Restock Level" field
    And I should see "Open_box" in the "Condition" dropdown
    And I should see "True" in the "Restocking Available" dropdown