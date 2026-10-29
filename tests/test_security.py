
import re

from playwright.sync_api import expect

from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.products_page import ProductsPage


def test_TC21_products_url_denied_after_logout(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.logout()

    # Confirm the user is redirected away from the inventory page.
    expect(page).not_to_have_url(re.compile(r".*/inventory\.html$"))

    # Attempt to access the protected page directly after logout.
    page.goto(f"{BASE_URL.rstrip('/')}/inventory.html")

    expect(page).not_to_have_url(re.compile(r".*/inventory\.html$"))
    expect(page.locator("#login-button")).to_be_visible()
