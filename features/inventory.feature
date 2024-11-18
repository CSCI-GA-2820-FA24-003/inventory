Feature: The inventory store service back-end
    As a Inventory Manager
    I need a RESTful catalog service
    So that I can keep track of all my inventories

Background:
    Given the following inventories
        | name       | quantity | restock level | condition  | restocking available   |
        | Juice      | 123      | 10            | NEW        | True                   |
        | Orange     | 444      | 90            | OPEN_BOX   | True                   |
        | Pencil     | 6666     | 30            | USED       | True                   |
        | Lighter    | 97645    | 10000         | USED       | False                  |

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

Scenario: Read a Inventory
    When I visit the "Home Page"
    And I set the "Name" to "Juice"
    And I press the "Search" button
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
    And I should see "Juice" in the "Name" field
    And I should see "123" in the "Quantity" field
    And I should see "10" in the "Restock Level" field
    And I should see "New" in the "Condition" dropdown
    And I should see "True" in the "Restocking Available" dropdown

Scenario: Update a Inventory
    When I visit the "Home Page"
    And I set the "Name" to "Juice"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Juice" in the "Name" field
    And I should see "123" in the "Quantity" field
    And I should see "10" in the "Restock Level" field
    And I should see "New" in the "Condition" dropdown
    And I should see "True" in the "Restocking Available" dropdown
    When I change "Name" to "Watermelon"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Watermelon" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Watermelon" in the results
    And I should not see "Juice" in the results

Scenario: Delete a Inventory 
    When I visit the "Home Page"
    And I set the "Name" to "Juice"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Juice" in the "Name" field
    And I should see "123" in the "Quantity" field
    And I should see "10" in the "Restock Level" field
    And I should see "New" in the "Condition" dropdown
    And I should see "True" in the "Restocking Available" dropdown
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Inventory has been Deleted!"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: List Inventory
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Juice" in the results
    And I should see "Orange" in the results
    And I should see "Pencil" in the results
    And I should not see "Lighter" in the results

Scenario: Search for name
    When I visit the "Home Page"
    And I set the "Name" to "Juice"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "123" in the results
    And I should see "Juice" in the results
    And I should not see "Orange" in the results
    And I should not see "Pencil" in the results
    And I should not see "Lighter" in the results

Scenario: Search for quantity
    When I visit the "Home Page"
    And I set the "Quantity" to "123"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "123" in the results
    And I should see "Juice" in the results
    And I should not see "Orange" in the results
    And I should not see "Pencil" in the results
    And I should not see "Lighter" in the results

Scenario: Search for restock level
    When I visit the "Home Page"
    And I set the "Restock Level" to "10"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "10" in the results
    And I should see "Juice" in the results
    And I should not see "Orange" in the results
    And I should not see "Pencil" in the results
    And I should not see "Lighter" in the results

Scenario: Search for condition
    When I visit the "Home Page"
    And I select "New" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "NEW" in the results
    And I should see "Juice" in the results
    And I should not see "Orange" in the results
    And I should not see "Pencil" in the results
    And I should not see "Lighter" in the results

Scenario: Search for restocking available
    When I visit the "Home Page"
    And I select "False" in the "Restocking Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "true" in the results
    And I should see "false" in the results
    And I should see "Juice" in the results
    And I should see "Orange" in the results
    And I should see "Pencil" in the results
    And I should see "Lighter" in the results

Scenario: Start Restocking
    When I visit the "Home Page"
    And I set the "Name" to "Juice"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Juice" in the "Name" field
    And I should see "123" in the "Quantity" field
    And I should see "10" in the "Restock Level" field
    And I should see "New" in the "Condition" dropdown
    And I should see "True" in the "Restocking Available" dropdown
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Start Restocking" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Juice" in the "Name" field
    And I should see "123" in the "Quantity" field
    And I should see "10" in the "Restock Level" field
    And I should see "New" in the "Condition" dropdown
    And I should see "False" in the "Restocking Available" dropdown
    When I press the "Start Restocking" button
    Then I should see the message "409"

Scenario: Stop Restocking
    When I visit the "Home Page"
    And I set the "Name" to "Lighter"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Lighter" in the "Name" field
    And I should see "97645" in the "Quantity" field
    And I should see "10000" in the "Restock Level" field
    And I should see "Used" in the "Condition" dropdown
    And I should see "False" in the "Restocking Available" dropdown
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Stop Restocking" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Lighter" in the "Name" field
    And I should see "97645" in the "Quantity" field
    And I should see "10000" in the "Restock Level" field
    And I should see "Used" in the "Condition" dropdown
    And I should see "True" in the "Restocking Available" dropdown
    When I press the "Stop Restocking" button
    Then I should see the message "409"