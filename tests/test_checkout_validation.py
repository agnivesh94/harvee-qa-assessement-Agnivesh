
import pytest

from config import STANDARD_USER, PASSWORD
from pages.products_page import ProductsPage
from pages.checkout_page import CheckoutPage


@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "expected_error"),
    [
        pytest.param(
            "", "Bhosale", "411001",
            "First Name is required",
            id="TC15_missing_first_name",
        ),
        pytest.param(
            "Agnivesh", "", "411001",
            "Last Name is required",
            id="TC16_missing_last_name",
        ),
        pytest.param(
            "Agnivesh", "Bhosale", "",
            "Postal Code is required",
            id="TC17_missing_postal_code",
        ),
    ],
)
def test_TC15_TC16_TC17_required_checkout_fields(
    page,
    login_page,
    first_name,
    last_name,
    postal_code,
    expected_error,
):
    login_page.login(STANDARD_USER, PASSWORD)

    products = ProductsPage(page)
    products.add_product_to_cart("Sauce Labs Backpack")
    products.open_cart()

    checkout = CheckoutPage(page)
    checkout.start_checkout()

    checkout.enter_customer_details(
        first_name,
        last_name,
        postal_code,
    )
    checkout.continue_to_overview()

    checkout.expect_checkout_error(expected_error)
