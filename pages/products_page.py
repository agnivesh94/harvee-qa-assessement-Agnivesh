
from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.sort_dropdown = page.locator(
            '[data-test="product-sort-container"]'
        )
        self.product_names = page.locator(
            '[data-test="inventory-item-name"]'
        )
        self.product_prices = page.locator(
            '[data-test="inventory-item-price"]'
        )
        self.cart_badge = page.locator(
            '[data-test="shopping-cart-badge"]'
        )
        self.cart_link = page.locator(
            '[data-test="shopping-cart-link"]'
        )

    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)

    def get_product_names(self) -> list[str]:
        return self.product_names.all_text_contents()

    def get_product_prices(self) -> list[float]:
        return [
            float(price.replace("$", ""))
            for price in self.product_prices.all_text_contents()
        ]

    def add_product_to_cart(self, product_name: str):
        product = self.page.locator(
            '[data-test="inventory-item"]'
        ).filter(has_text=product_name)

        product.locator("button").click()

    def open_cart(self):
        self.cart_link.click()

    def expect_cart_count(self, count: int):
        if count == 0:
            expect(self.cart_badge).to_have_count(0)
        else:
            expect(self.cart_badge).to_have_text(str(count))
            
            
    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("#logout_sidebar_link").click()

