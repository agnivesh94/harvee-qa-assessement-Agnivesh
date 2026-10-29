
from pathlib import Path

import pytest
from playwright.sync_api import Page

from config import BASE_URL
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page):
    login = LoginPage(page)
    login.open(BASE_URL)
    return login


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = screenshot_dir / f"{item.name}.png"

            try:
                page.screenshot(
                    path=str(screenshot_path),
                    full_page=True,
                )
                print(f"Failure screenshot saved: {screenshot_path}")
            except Exception as error:
                print(f"Could not save failure screenshot: {error}")
