# Harvee Technologies – QA Automation Assessment

## Overview

This repository contains manual test cases and UI automation tests for the Sauce Demo application.

The automation framework uses Python, Playwright, pytest, and the Page Object Model (POM) design pattern.

## Technology Stack

- Python
- Playwright (Python API)
- pytest
- pytest-html
- Chromium browser
- Git

## Prerequisites

- Python installed and available on PATH
- Git installed
- Visual Studio Code (recommended)
- Internet access to reach https://www.saucedemo.com

## Project Structure

```text
harvee-qa-assessement-Agnivesh/
├── config.py
├── conftest.py
├── pages/
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_products.py
│   ├── test_checkout.py
│   ├── test_checkout_validation.py
│   └── test_security.py
├── MANUAL_TEST_CASES.md
├── README.md
├── ANSWERS.md
├── AI_USAGE.md
└── report.html
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd harvee-qa-assessement-Agnivesh
```

Replace `<your-repository-url>` with the URL of your Git repository.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the required packages:

```powershell
python -m pip install pytest pytest-playwright pytest-html pytest-base-url
python -m playwright install chromium
```

## Configuration

The application URL and test credentials are configured in `config.py`. Environment variables can override the defaults.

Available variables:

- `SAUCEDEMO_BASE_URL`
- `SAUCEDEMO_STANDARD_USER`
- `SAUCEDEMO_LOCKED_OUT_USER`
- `SAUCEDEMO_PASSWORD`

Example for PowerShell:

```powershell
$env:SAUCEDEMO_BASE_URL="https://www.saucedemo.com"
```

Use only authorized test accounts. Avoid committing real credentials or secrets.

## Running Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Generate a self-contained HTML report:

```powershell
python -m pytest -v --html=report.html --self-contained-html
```

The report is generated as `report.html` in the repository root.

Run a specific test file:

```powershell
python -m pytest tests/test_login.py -v
```

Run a specific test by its name:

```powershell
python -m pytest -k "locked_out" -v
```


# Automated Test Coverage

The automation suite contains 10 test functions and 12 executed test cases. The checkout validation test is parameterized to cover three scenarios (TC15, TC16, and TC17).

| Manual Test ID | Scenario | Automation File | Automated Test Name |
|---|---|---|---|
| TC01 | Standard user login | `tests/test_login.py` | `test_TC01_standard_user_logs_in` |
| TC02 | Locked-out user login | `tests/test_login.py` | `test_TC02_locked_out_user_cannot_log_in` |
| TC03 | Invalid credentials rejected | `tests/test_login.py` | `test_TC03_invalid_credentials_rejected` |
| TC06 | Sort products by price, low to high | `tests/test_products.py` | `test_TC06_sort_price_low_to_high` |
| TC08 | Sort products by name, A to Z | `tests/test_products.py` | `test_TC08_sort_name_a_to_z` |
| TC10 | Add two products and remove one from the Products page | `tests/test_products.py` | `test_TC10_add_two_remove_one_and_verify_cart` |
| TC11 | Remove an item from the Cart page | `tests/test_products.py` | `test_TC11_remove_item_from_cart` |
| TC15, TC16, TC17 | Checkout required-field validation | `tests/test_checkout_validation.py` | `test_TC15_TC16_TC17_required_checkout_fields` |
| TC19 | Complete checkout, verify totals and confirmation, and empty the cart | `tests/test_checkout.py` | `test_TC19_complete_checkout_totals_and_empty_cart` |
| TC21 | Products URL denied after logout | `tests/test_security.py` | `test_TC21_products_url_denied_after_logout` |

## Test Execution

Run all automated tests:

```powershell
python -m pytest tests/ -v
```

Generate a self-contained HTML report:

```powershell
python -m pytest tests/ -v --html=report.html --self-contained-html
```

Open the report:

```powershell
start report.html
```

## Latest Verified Result

- Automated test functions: 10
- Executed test cases: 12
- Passed: 12
- Failed: 0

The latest full test run completed successfully in 11.74 seconds. Rerun the suite before submission if any code changes are made.


## Manual Testing

The manual test suite is documented in `MANUAL_TEST_CASES.md`. It contains the test scenarios, expected results, and automation mapping.

## Framework Design

- **Page Object Model:** Page-specific locators and actions are encapsulated in page classes.
- **Reusable fixtures:** `conftest.py` provides shared setup.
- **Independent tests:** Each test establishes the required application state.
- **Assertions:** pytest and Playwright assertions verify expected outcomes.
- **Failure evidence:** A pytest hook attempts to capture a full-page screenshot when a test fails during execution.
- **Reporting:** pytest-html generates an HTML execution report.

## Scaling the Framework to 200 Tests

To support approximately 200 tests while maintaining readability and reliability:

1. Organize tests by feature, such as authentication, products, cart, checkout, and access control.
2. Extend the Page Object Model and reuse common components and actions.
3. Use pytest fixtures for shared setup, teardown, and test data.
4. Parameterize similar scenarios to reduce duplication.
5. Keep test data separate from test logic and use environment variables for configuration.
6. Add API tests for suitable backend workflows.
7. Run tests in CI/CD and publish HTML or JUnit reports.
8. Use markers to separate smoke, regression, and slower tests.
9. Capture screenshots, traces, and logs for failures.
10. Monitor flaky tests and fix their underlying causes instead of repeatedly retrying them.

## Current Execution Result

The current suite contains 10 automated test cases, including parameterized checkout validation scenarios.

Latest verified run:

- Passed: 10
- Failed: 0
- Duration: approximately 9 seconds

The results above describe the latest local run and may differ on subsequent executions.
