from config import STANDARD_USER, PASSWORD
from pages.products_page import ProductsPage
from pages.cart_page import CartPage


def test_TC06_sort_price_low_to_high(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.sort_by("lohi")

    prices = products.get_product_prices()

    # Verify the entire list is sorted in ascending order.
    assert len(prices) > 1, "Expected multiple products"
    assert prices == sorted(prices), (
        f"Products are not sorted low to high: {prices}"
    )


def test_TC10_add_two_remove_one_and_verify_cart(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.add_product_to_cart("Sauce Labs Backpack")
    products.add_product_to_cart("Sauce Labs Bike Light")

    products.expect_cart_count(2)
    products.open_cart()

    cart = CartPage(page)
    cart.expect_product_count(2)
    cart.expect_product_present("Sauce Labs Backpack")
    cart.expect_product_present("Sauce Labs Bike Light")

    cart.remove_product("Sauce Labs Backpack")

    cart.expect_product_count(1)
    cart.expect_product_absent("Sauce Labs Backpack")
    cart.expect_product_present("Sauce Labs Bike Light")


def test_TC08_sort_name_a_to_z(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.sort_by("az")

    names = products.get_product_names()

    # Verify the complete product-name sequence.
    assert len(names) > 1, "Expected multiple products"
    assert names == sorted(names, key=str.casefold), (
        f"Products are not sorted A to Z: {names}"
    )
    
    
    
def test_TC11_remove_item_from_cart(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.add_product_to_cart("Sauce Labs Backpack")
    products.add_product_to_cart("Sauce Labs Bike Light")
    products.open_cart()

    cart = CartPage(page)

    # Verify both products are initially present.
    cart.expect_product_count(2)
    cart.expect_product_present("Sauce Labs Backpack")
    cart.expect_product_present("Sauce Labs Bike Light")

    # Remove one item from the Cart page.
    cart.remove_product("Sauce Labs Backpack")

    # Verify the remaining cart contents and badge.
    cart.expect_product_count(1)
    cart.expect_product_absent("Sauce Labs Backpack")
    cart.expect_product_present("Sauce Labs Bike Light")
    products.expect_cart_count(1)

