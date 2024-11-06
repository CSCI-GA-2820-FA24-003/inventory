# NYU FA24 DevOps Inventory

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-FA24-003/inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA24-003/inventory/actions)
[![codecov](https://codecov.io/github/CSCI-GA-2820-FA24-003/inventory/graph/badge.svg?token=OYYDZUE3PA)](https://codecov.io/github/CSCI-GA-2820-FA24-003/inventory)
![image](https://media.istockphoto.com/id/589106848/vector/isometric-warehouse-manager-or-worker-with-bar-code-scanner-checking.jpg?s=612x612&w=0&k=20&c=rOiV2anxSL2mqDjN1ubXEe-u0DG916v4QPdLT_FfgrU=)


## Catalog
- [NYU FA24 DevOps Inventory](#nyu-fa24-devops-inventory)
  - [Catalog](#catalog)
  - [1 Overview](#1-overview)
  - [2 Preparation](#2-preparation)
    - [2.1 Prerequisites](#21-prerequisites)
    - [2.2 Running the Service](#22-running-the-service)
  - [3 Contents](#3-contents)
  - [4 Testing](#4-testing)
    - [4.1 Test with Container](#41-test-with-container)
    - [4.2 Test with Endpoints](#42-test-with-endpoints)
  - [5 Coding Rules](#5-coding-rules)
    - [5.1 Python Style Guide](#51-python-style-guide)
    - [5.2 Naming Conventions](#52-naming-conventions)
    - [5.3 Comments](#53-comments)
    - [5.4 Error Handling](#54-error-handling)
    - [5.5 Imports](#55-imports)
    - [5.6 Testing Standard](#56-testing-standard)
    - [5.7 Version Control](#57-version-control)
    - [5.8 Code Organization](#58-code-organization)
    - [5.9 Documentation](#59-documentation)
  - [6 License](#6-license)
## 1 Overview

The inventory project is a microservice that helps the user to keep track of inventories in the database. Its functionalities include listing inventory information, adding inventory to the database and deleting inventory items from the database.

## 2 Preparation
### 2.1 Prerequisites

- Python 3.11
- Poetry for Python package management
  
### 2.2 Running the Service

To get the service go: `http://localhost:8080`.
Environment defined in `.flaskenv` file used to load configuration.
Run the service by entering 
```bash
flask run
```
in terminal.

## 3 Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

.github/                   - folder for CI
└── ISSUE_TEMPLATE         - Templates for Zenhub items
    ├── bug_report.md      - Template for bug reports
    ├── user-story.md      - Template for user stories

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```
## 4 Testing
### 4.1 Test with Container
Navigate to terminal and type
```bash
pytest
```
The terminal will run and complete test automatically.

### 4.2 Test with Endpoints
| Method | Endpoint Command                         | Function                                | Status                                  |  Response (Example)                                                |
|--------|------------------------------------------|-----------------------------------------|--------------------------------------------|------------------------------------------------------------------|
| GET    | `http://localhost:8080/inventories`      | List all inventories                    | `200 OK` | `[ { "condition": "NEW", "id": 838, "name": "Sample Inventory", "quantity": 100,"restock level": 50 }, ... ]` |
| POST   | `http://localhost:8080/inventories`      | Create a new inventory item             | `201 CREATED`| `{"name": "Sample Inventory", "quantity": 100, "location": "Warehouse A", "restock_level": 50, "condition": "new"}`          |
| GET    | `http://localhost:8080/inventories/838` | Retrieve an inventory item by id        | `200 OK`             | `{"condition": "NEW", "id": 838, "name": "Sample Inventory", "quantity": 100, "restock_level": 50}`          |
| PUT    | `http://localhost:8080/inventories/838` | Update an existing inventory item by id | `200 OK` | `{"condition": "NEW", "id": 838, "name": "Sample Inventory", "quantity": 200, "restock_level": 50}`          |
| DELETE | `http://localhost:8080/inventories/838` | Delete an inventory item by id          | `204 NO CONTENT` |     |

## 5 Coding Rules

To ensure consistency and maintainability across our codebase, all developers should adhere to the following coding rules and conventions:

### 5.1 Python Style Guide 
Follow PEP 8 guidelines: 
   - Use 4 spaces for indentation (no tabs)
   - Maximum line length of 79 characters
   - For long block comments or docstrings, limit to 72 characters
   - Two blank lines between top-level functions and classes
   - One blank line between methods in a class
   - Imports should usually be on separate lines

### 5.2 Naming Conventions
   - Classes: Use CamelCase (e.g., `MyClass`)
   - Functions and variables: Use snake_case (e.g., `my_function`, `my_variable`)
   - Constants: Use uppercase with underscores (e.g., `MAX_VALUE`)

### 5.3 Comments
   - Write clear, concise comments for complex logic
   - Avoid obvious comments

### 5.4 Error Handling
   - Use try-except blocks for error handling
   - Avoid bare except clauses

### 5.5 Imports
   - Group imports in the following order: standard library, third-party, local application
   - Use absolute imports when possible

### 5.6 Testing Standard
   - Write unit tests for all new functionality
   - Maintain a minimum of 95% code coverage

### 5.7 Version Control
   - Write clear, descriptive commit messages
   - Create feature branches for new work
   - Use pull requests for code reviews

### 5.8 Code Organization
   - Keep functions and methods small and focused
   - Use meaningful names for variables and functions

### 5.9 Documentation
   - Keep this README updated with any new setup steps or important information
   - Document any non-obvious design decisions or algorithms
   
## 6 License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
