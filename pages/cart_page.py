
from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(
            '[data-test="inventory-item"]'
        )
        self.cart_badge = page.locator(
            '[data-test="shopping-cart-badge"]'
        )

    def remove_product(self, product_name: str):
        item = self.page.locator(
            '[data-test="inventory-item"]'
        ).filter(has_text=product_name)

        item.locator("button").click()

    def expect_product_count(self, count: int):
        expect(self.cart_items).to_have_count(count)

    def expect_product_present(self, product_name: str):
        expect(
            self.page.locator('[data-test="inventory-item"]')
            .filter(has_text=product_name)
        ).to_be_visible()

    def expect_product_absent(self, product_name: str):
        expect(
            self.page.locator('[data-test="inventory-item"]')
            .filter(has_text=product_name)
        ).to_have_count(0)
