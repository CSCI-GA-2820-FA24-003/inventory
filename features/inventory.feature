Feature: The inventory store service back-end
    As a Inventory Manager
    I need a RESTful catalog service
    So that I can keep track of all my inventories

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"
