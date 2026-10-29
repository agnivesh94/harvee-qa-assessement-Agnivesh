
import re

from playwright.sync_api import expect

from config import STANDARD_USER, LOCKED_OUT_USER, PASSWORD


def test_TC01_standard_user_logs_in(login_page, page):
    login_page.login(STANDARD_USER, PASSWORD)

    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")


def test_TC02_locked_out_user_cannot_log_in(login_page, page):
    login_page.login(LOCKED_OUT_USER, PASSWORD)

    login_page.expect_login_error("locked out")
    expect(page).not_to_have_url(re.compile(r".*/inventory\.html$"))


def test_TC03_invalid_credentials_rejected(login_page, page):
    login_page.login("invalid_user", "wrong_password")

    login_page.expect_login_error("Username and password do not match")
    expect(page).not_to_have_url(re.compile(r".*/inventory\.html$"))
