# NYU DevOps Inventory FA24

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-FA24-003/inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA24-003/inventory/actions)
![image](https://www.munim-ji.com/wp-content/uploads/2023/01/png-clipart-clipboard-with-box-art-inventory-management-software-point-of-sale-e-commerce-warehouse-miscellaneous-text.png)

## Overview

The inventory project is a microservice that helps the user to keep track of inventories in the database. Its functionalities include listing inventory information, adding inventory to the database and deleting inventory items from the database.

## Prerequisites

- Python 3.11
- Poetry for Python package management
  
## Running the service

The project uses `honcho` which gets its commands from the `Procfile`. To start the service simply use:

```shell
honcho start
```

To get the service go: `http://localhost:8000`.
Environment defined in `.flaskenv` file used to load configuration.

## Contents

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

## Coding Rules

To ensure consistency and maintainability across our codebase, all developers should adhere to the following coding rules and conventions:

1. **Python Style Guide**: Follow PEP 8 guidelines for Python code style. This includes:
   - Use 4 spaces for indentation (no tabs)
   - Maximum line length of 79 characters
   - For long block comments or docstrings, limit to 72 characters
   - Two blank lines between top-level functions and classes
   - One blank line between methods in a class
   - Imports should usually be on separate lines

2. **Naming Conventions**:
   - Classes: Use CamelCase (e.g., `MyClass`)
   - Functions and variables: Use snake_case (e.g., `my_function`, `my_variable`)
   - Constants: Use uppercase with underscores (e.g., `MAX_VALUE`)

3. **Comments**:
   - Write clear, concise comments for complex logic
   - Avoid obvious comments

4. **Error Handling**: 
   - Use try-except blocks for error handling
   - Avoid bare except clauses

5. **Imports**: 
   - Group imports in the following order: standard library, third-party, local application
   - Use absolute imports when possible

6. **Testing**:
   - Write unit tests for all new functionality
   - Maintain a minimum of 90% code coverage

7. **Version Control**:
   - Write clear, descriptive commit messages
   - Create feature branches for new work
   - Use pull requests for code reviews

8. **Code Organization**:
   - Keep functions and methods small and focused
   - Use meaningful names for variables and functions

9. **Documentation**:
    - Keep this README updated with any new setup steps or important information
    - Document any non-obvious design decisions or algorithms
   
## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
