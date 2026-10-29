
from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

        self.checkout_button = page.locator(
            '[data-test="checkout"]'
        )
        self.first_name = page.locator(
            '[data-test="firstName"]'
        )
        self.last_name = page.locator(
            '[data-test="lastName"]'
        )
        self.postal_code = page.locator(
            '[data-test="postalCode"]'
        )
        self.continue_button = page.locator(
            '[data-test="continue"]'
        )
        self.finish_button = page.locator(
            '[data-test="finish"]'
        )
        self.item_total = page.locator(
            '[data-test="subtotal-label"]'
        )
        self.tax = page.locator(
            '[data-test="tax-label"]'
        )
        self.total = page.locator(
            '[data-test="total-label"]'
        )
        self.complete_header = page.locator(
            '[data-test="complete-header"]'
        )
        self.error_message = page.locator(
            '[data-test="error"]'
        )

    def start_checkout(self):
        self.checkout_button.click()

    def enter_customer_details(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def continue_to_overview(self):
        self.continue_button.click()

    def finish_order(self):
        self.finish_button.click()

    def get_money_value(self, locator) -> float:
        text = locator.inner_text()
        return float(text.split("$")[-1])

    def expect_order_complete(self):
        expect(self.complete_header).to_have_text(
            "Thank you for your order!"
        )
        
        
    def expect_checkout_error(self, message: str):
        expect(self.error_message).to_contain_text(message)

