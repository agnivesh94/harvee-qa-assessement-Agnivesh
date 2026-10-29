
import re

from playwright.sync_api import expect

from config import STANDARD_USER, PASSWORD
from pages.products_page import ProductsPage
from pages.checkout_page import CheckoutPage


def test_TC19_complete_checkout_totals_and_empty_cart(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.add_product_to_cart("Sauce Labs Backpack")
    products.add_product_to_cart("Sauce Labs Bike Light")
    products.open_cart()

    checkout = CheckoutPage(page)
    checkout.start_checkout()

    checkout.enter_customer_details(
        "Agnivesh",
        "Bhosale",
        "411001",
    )
    checkout.continue_to_overview()

    expect(page).to_have_url(
        re.compile(r".*/checkout-step-two\.html$")
    )

    item_total = checkout.get_money_value(checkout.item_total)
    tax = checkout.get_money_value(checkout.tax)
    total = checkout.get_money_value(checkout.total)

    # Allow for currency rounding to two decimal places.
    assert round(item_total + tax, 2) == round(total, 2), (
        f"Expected item total + tax = total; "
        f"got {item_total} + {tax} != {total}"
    )

    checkout.finish_order()
    checkout.expect_order_complete()

    # The cart should be empty after placing the order.
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)

    products.open_cart()
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(0)
