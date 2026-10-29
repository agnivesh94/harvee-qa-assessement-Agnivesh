# Section B – AI Output and Client Communication

## B1. Review AI-Generated Code

### Problems identified

1. **Malformed URL:** Markdown-link syntax is used instead of the actual URL.
2. **Hard-coded configuration:** URL and credentials should come from configuration or environment variables.
3. **Ambiguous locator:** `text=Add to cart` may match multiple products.
4. **No login assertion:** The test does not verify successful login or the Products page.
5. **No cart assertion:** It does not verify that the intended product was added.
6. **Fixed sleep:** `waitForTimeout(3000)` is slow and potentially flaky. Use Playwright auto-waiting and assertions.
7. **Cart state not verified:** The test does not establish and check the expected cart contents before checkout.
8. **Unexplained test data:** One-character names and postal code may be unrealistic or unsuitable.
9. **Missing navigation assertions:** Checkout page transitions are not verified.
10. **Weak total assertion:** `toBeTruthy()` proves only that some text exists, not that the total is correct.
11. **No arithmetic validation:** Subtotal plus tax is not compared with the displayed total.
12. **Money parsing risks:** Currency values should be parsed carefully to avoid floating-point errors.
13. **No Page Object Model:** Locators and actions are embedded directly in the test.
14. **No order confirmation assertion:** The test does not complete the order or verify confirmation.
15. **No empty-cart assertion:** It does not verify the final cart state.
16. **No failure evidence or reporting shown:** The snippet does not demonstrate screenshots or test reports.
17. **Poor failure diagnosis:** Missing intermediate assertions can cause failures to appear far from their root cause.

### Rewritten test — Python + Playwright + pytest

The test below uses the existing Page Object Model and verifies the actual checkout total rather than simply checking that total text exists.

```python
import re
from decimal import Decimal

from playwright.sync_api import Page, expect

from config import STANDARD_USER, PASSWORD
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def money_to_cents(text: str) -> int:
    match = re.search(r"\$([\d,]+\.\d{2})", text)
    assert match, f"Could not parse currency from: {text!r}"
    amount = Decimal(match.group(1).replace(",", ""))
    return int(amount * 100)


def test_TC05_complete_checkout_and_verify_total(
    page: Page, login_page
):
    # Log in and verify the Products page.
    login_page.login(STANDARD_USER, PASSWORD)
    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")

    # Add two specific products and verify the cart.
    products = ProductsPage(page)
    products.add_product_to_cart("Sauce Labs Backpack")
    products.add_product_to_cart("Sauce Labs Bike Light")
    products.expect_cart_count(2)
    products.open_cart()

    cart = CartPage(page)
    cart.expect_product_count(2)

    # Complete checkout with valid test data.
    checkout = CheckoutPage(page)
    checkout.start_checkout()
    checkout.enter_customer_details(
        first_name="Agnivesh",
        last_name="Bhosale",
        postal_code="411001",
    )
    checkout.continue_to_overview()

    expect(page).to_have_url(
        re.compile(r".*/checkout-step-two\.html$")
    )

    # Compare displayed monetary amounts using integer cents.
    subtotal_cents = money_to_cents(
        checkout.subtotal.inner_text()
    )
    tax_cents = money_to_cents(checkout.tax.inner_text())
    total_cents = money_to_cents(checkout.total.inner_text())

    assert subtotal_cents + tax_cents == total_cents, (
        f"Incorrect total: subtotal={subtotal_cents}, "
        f"tax={tax_cents}, total={total_cents} cents"
    )

    # Finish the order and verify the outcome.
    checkout.finish_order()
    checkout.expect_order_complete()

    products.open_cart()
    expect(
        page.locator('[data-test="inventory-item"]')
    ).to_have_count(0)
```
Language choice: The original example uses Playwright's JavaScript/TypeScript syntax. I have rewritten it in Python with Playwright and pytest to match the framework used in this assessment repository. The rewritten test uses existing page objects and shared configuration.

## B2. Test an AI Feature – Test Case Generator

| Check | Evaluation design | Scoring |
|---|---|---|
| Requirement coverage | Use gold-standard stories covering positive, negative, boundary, permission, and error scenarios. Measure required-scenario recall. | Automated coverage calculation with reviewer validation. |
| No invented requirements | Use stories with deliberate gaps and identify unsupported business rules. | Human rubric: 0 = none, 1 = minor, 2 = material invention. |
| Duplicate cases | Detect exact duplicates and review semantically similar cases. | Automatic exact-match detection plus human review of near-duplicates. |
| Valid JSON schema | Validate JSON syntax, required keys, data types, allowed values, and escaping. | Automated pass/fail; zero tolerance for invalid JSON. |

The evaluation set should include both straightforward and ambiguous user stories so that the generator is tested against realistic conditions.

## B3. Jira Defect Report

**Title:** [Catalog][Sorting] Price low-to-high displays $29.99 before $15.99 in release 4.2.0

**Environment**
- Application: Sauce Demo practice site
- Release: 4.2.0
- Browser: Chrome — record the exact version
- Operating system: Record the exact OS version
- User: standard_user
- Viewport: Desktop

**Preconditions**
- The user is logged in.
- The Products page is displayed.

**Steps to reproduce**
1. Open the Products page.
2. Open the sorting dropdown.
3. Select **Price (low to high)**.
4. Inspect the product prices from top to bottom.
5. Repeat the steps to confirm reproducibility.

**Expected result**

All products appear in numeric ascending order. Each price is less than or equal to the next price.

**Actual result**

An item priced at $29.99 appears before an item priced at $15.99. The issue has occurred on every observed run since release 4.2.0.

**Severity: Major / High (proposed)**

The defect affects a core shopping function and contradicts the selected sorting option, potentially misleading customers. Critical severity is not justified by the current evidence because checkout is not reported to be blocked.

**Priority: P1 (proposed)**

Recommend urgent release triage because the defect is reproducible and customer-visible. Final priority should follow the client's guidelines.

**Evidence to attach**
- Screenshot showing the selected sorting option and incorrect order.
- Short screen recording of the issue.
- Full displayed price sequence.
- Exact browser version, OS, and application build.
- Reproduction count and relevant console or network logs, if available.

## B4. Message to the Client

Hi, our checks have identified two risks ahead of Friday's release. First, price sorting is consistently incorrect: a $29.99 item appears before a $15.99 item. Second, one checkout test fails about 1 in 10 runs, although it passes when repeated. We need to investigate whether the checkout issue is a product problem or test/environment instability.

**My recommendation is not to release version 4.2.0 unchanged.** The safest option is to fix the sorting defect and rerun focused checkout and regression tests. If Friday's date cannot move, we could consider disabling the faulty sort option, if the product supports that safely, but only after investigating the checkout failures and agreeing on monitoring and rollback criteria.

I'll share the evidence and a go/no-go recommendation by an agreed time today. Can we confirm the acceptable fallback?