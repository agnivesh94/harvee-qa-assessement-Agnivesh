# Section A1 — Manual Test Suite: Shop and Check Out

**Application:** https://www.saucedemo.com/  
**Scope:** Login, product browsing and sorting, cart management, checkout, order confirmation, session/security behavior, usability, responsive layout, and accessibility.  
**Test type:** Manual functional and non-functional testing.  
**Environment assumption:** Current stable desktop Chrome, with a second pass at a narrow/mobile viewport where specified. Use only the Sauce Demo public practice site.

## 1. Questions for the product owner and assumptions

| # | Question for product owner | Assumption to test until clarified |
|---|---|---|
| Q1 | Should usernames and passwords be case-sensitive? | Credentials are case-sensitive; only the exact valid credentials should work. |
| Q2 | What validation rules apply to postal codes (country-specific format, length, or characters)? | Postal code is required; any non-empty value is accepted unless the application displays a stricter rule. |
| Q3 | Should the cart persist after logout and a subsequent login? | Do not assume persistence; record observed behavior and confirm expected behavior with the product owner. |
| Q4 | Can a customer change item quantities in the cart, or only add/remove products? | Quantity is controlled by adding or removing products; no quantity-edit control is required by this use case. |
| Q5 | How should tax be calculated and rounded? | The overview tax should match the application’s displayed calculation and rounding; total must equal displayed item total plus displayed tax. |
| Q6 | Should checkout prevent duplicate orders if Finish is clicked repeatedly or the page is refreshed? | A completed checkout should not create duplicate orders; verify behavior if safe and practical in the practice site. |
| Q7 | Which browsers and minimum viewport sizes are officially supported? | Test in current desktop Chrome and check a narrow 375 px viewport for usability; confirm the formal browser matrix. |
| Q8 | What accessibility conformance level is required (for example, WCAG 2.2 AA)? | Perform basic keyboard-only and visible-focus checks; a full WCAG audit is outside this time-boxed suite. |
| Q9 | What should happen when a logged-out user directly opens a protected page URL? | The user should be redirected to login or otherwise denied access to protected content. |
| Q10 | Should the locked-out account show a specific error message, and should it reveal account status? | The locked-out account is denied access with a clear error; verify the displayed message without assuming broader security policy. |

## 2. Test cases

**Priority guide:** P1 = critical purchase path/security; P2 = important functional behavior; P3 = usability or lower-risk coverage.  
**Automation note:** “Yes” means suitable for repeatable UI regression automation. “No” means better kept manual or evaluated at another layer for this assessment.

| ID | Area | Type | Title | Pre-conditions | Steps | Test data | Expected result | Priority | Automate? and why |
|---|---|---|---|---|---|---|---|---|---|
| TC01 | Login | Positive | Standard user logs in successfully | Logged out; login page open | Enter valid username and password; click Login | `standard_user` / shared password shown on site | User reaches Products page and product inventory is visible | P1 | Yes — core smoke path |
| TC02 | Login | Negative | Locked-out user cannot log in | Logged out; login page open | Enter locked-out username and shared password; click Login | `locked_out_user` / shared password shown on site | Login is rejected and a clear error message is displayed; Products page is not opened | P1 | Yes — required negative regression |
| TC03 | Login | Negative | Invalid credentials are rejected | Logged out; login page open | Enter an invalid username and password; click Login | `invalid_user` / `wrong_password` | Login is rejected with an error; no authenticated page is shown | P1 | Yes — validates negative login handling |
| TC04 | Login | Boundary/validation | Empty login fields are rejected | Logged out; login page open | Leave both fields empty; click Login | Blank username and password | Login is not successful and required-field/error feedback is shown | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC05 | Products | Positive | Product inventory displays product information | Logged in as standard user | Inspect several product cards | Standard user; default inventory | Each product shows its name, price, and expected product imagery/details; layout is readable | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC06 | Sorting | Positive | Sort products by price low to high | Logged in; Products page open | Choose Price (low to high); record all displayed prices; verify each adjacent pair is non-decreasing | Entire inventory price list | Every product is in ascending price order, including ties; no product is missing or duplicated | P1 | Yes — explicitly required; validate whole list |
| TC07 | Sorting | Positive | Sort products by price high to low | Logged in; Products page open | Choose Price (high to low); record all displayed prices; verify each adjacent pair is non-increasing | Entire inventory price list | Every product is in descending price order, including ties; no product is missing or duplicated | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC08 | Sorting | Positive | Sort products by name A to Z | Logged in; Products page open | Choose Name (A to Z); compare the complete displayed name sequence alphabetically | All product names | Names appear in ascending alphabetical order; no item is missing or duplicated | P2 | Yes — deterministic regression |
| TC09 | Sorting | Positive | Sort products by name Z to A | Logged in; Products page open | Choose Name (Z to A); compare the complete displayed name sequence in reverse alphabetical order | All product names | Names appear in descending alphabetical order; no item is missing or duplicated | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC10 | Cart | Positive | Add two products and remove one from Products page | Logged in; cart initially empty | Add two different products; verify badge; remove one from its product card; verify badge again; open cart | Two distinct products | Badge changes 0 → 1 → 2 → 1; cart contains only the remaining product | P1 | Yes — explicitly required end-to-end cart behavior |
| TC11 | Cart | Positive | Remove an item from the Cart page | Logged in; at least one product added | Open cart; click Remove for one item | One or more products | Removed product disappears and badge/count reflects remaining cart items | P2 | Yes — covers second removal location |
| TC12 | Cart | Boundary | Cart badge is absent or zero when cart is empty | Logged in; no products added, or all items removed | Inspect header before adding items and after removing all items | Empty cart | Badge behavior matches the app’s design (absent or zero); no stale positive count remains | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC13 | Navigation | Positive | Continue Shopping returns to inventory | Logged in; Cart page open | Click Continue Shopping | Cart with zero or more items | Products page opens and existing cart contents are retained | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC14 | Checkout | Positive | Checkout can start from a non-empty cart | Logged in; one or more items in cart | Open cart; click Checkout | One product in cart | Checkout information page opens and customer detail fields are available | P1 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC15 | Checkout validation | Negative | Missing first name is rejected | Logged in; item in cart; checkout information page open | Leave first name blank; enter last name and postal code; click Continue | First name blank; other fields populated | Checkout does not proceed; a clear validation message is displayed | P1 | Yes — include in one parameterized validation test |
| TC16 | Checkout validation | Negative | Missing last name is rejected | Logged in; item in cart; checkout information page open | Enter first name and postal code; leave last name blank; click Continue | Last name blank; other fields populated | Checkout does not proceed; a clear validation message is displayed | P1 | Yes — include in one parameterized validation test |
| TC17 | Checkout validation | Negative | Missing postal code is rejected | Logged in; item in cart; checkout information page open | Enter first and last name; leave postal code blank; click Continue | Postal code blank; other fields populated | Checkout does not proceed; a clear validation message is displayed | P1 | Yes — include in one parameterized validation test |
| TC18 | Checkout | Boundary | Postal code accepts a minimally valid non-empty value | Logged in; item in cart; checkout information page open | Enter first name, last name and a short non-empty postal code; click Continue | Example: first `Alex`, last `Tester`, postal code `1` | Behavior matches the agreed postal-code rule; under the current assumption, the form proceeds because the field is non-empty | P2 | No — boundary rule needs product-owner confirmation |
| TC19 | Checkout | Positive | Complete checkout and verify totals and cart is emptied | Logged in; one or more known products in cart | Continue from cart; enter customer details; click Continue; calculate item-price sum; verify item total, tax and total; click Finish; inspect confirmation and cart | Known products; valid first/last name and postal code | Overview lists expected items; item total matches sum of prices; total equals displayed item total + displayed tax; order confirmation appears; returning to cart shows it empty | P1 | Yes — explicitly required full checkout |
| TC20 | Checkout | Negative/navigation | Cancel checkout overview without placing order | Logged in; item in cart; overview page open | Click Cancel | One product in cart | User returns to the expected prior shopping/cart page; no order confirmation appears and order is not placed; verify cart state | P2 | No — outside the initial 10-test automation scope; retain as manual/future regression coverage |
| TC21 | Security/session | Negative/security | Protected Products URL is denied after logout | Logged in as standard user | Log out; type the Products page URL directly in the address bar and press Enter | Logged-out session; Products URL | Products content is not accessible; user is redirected to login or access is otherwise denied | P1 | Yes — explicitly required security regression |
| TC22 | Usability | Usability | Main shopping and checkout controls are understandable | Logged in as standard user | Without instructions, locate sorting, add/remove, cart, checkout, continue shopping and cancel controls; note unclear labels or feedback | Standard user; desktop viewport | Primary actions are discoverable, labels are understandable, and state changes (such as add/remove) are apparent | P3 | No — exploratory human observation is more useful |
| TC23 | Responsive/browser | Compatibility | Shopping flow remains usable at narrow viewport | Logged in; browser developer tools available | Set viewport to 375 × 667; inspect inventory, sorting, cart and checkout; attempt key actions | 375 × 667 viewport; current Chrome | No critical controls are hidden or unusable; content remains readable without unintended overlap or horizontal scrolling that blocks tasks | P2 | No — visual/layout assessment; automate only with visual tooling if needed |
| TC24 | Accessibility | Accessibility | Core flow is operable using keyboard only | Logged out; login page open | Use Tab/Shift+Tab to move through controls; use keyboard to log in, sort, add item, open cart and proceed through checkout; observe focus | Standard user; keyboard only | Focus is visible and follows a logical order; interactive controls can be reached and activated without a mouse; no keyboard trap occurs | P2 | No — manual accessibility check for focus and operability |

## 3. 15-minute exploratory testing charter — users with known problems

**Charter:** Explore whether Sauce Demo’s known-problem accounts expose inconsistent behavior in login, inventory, product images/details, cart operations, sorting, and checkout. Do not assume every defect is present; record observed evidence.

**Time box:** 15 minutes.  
**Test data:** Use only the public site’s listed accounts and shared password. Prioritize `problem_user`, then `performance_glitch_user`; if time permits, inspect `error_user` and `visual_user`. Do not use any other live system.

**Session plan:**
- **Minutes 0–3:** Log in with `problem_user`; compare product names, images and prices against the standard-user view where practical.
- **Minutes 3–6:** Add and remove multiple items; watch for incorrect button behavior, badge counts, or cart contents.
- **Minutes 6–9:** Exercise all available sort options; check the complete sequence, not only the first item.
- **Minutes 9–12:** Start checkout and try valid and missing-field data; look for hangs, incorrect navigation, or inconsistent validation.
- **Minutes 12–15:** If time permits, repeat a short flow with `performance_glitch_user`; capture any long delays or visual inconsistencies and note which account was used.

**Record for each finding:** account, time, steps, expected vs actual result, screenshot, reproducibility, severity/impact, and whether the same flow works with `standard_user`. Treat slow responses as observations, not confirmed defects, until reproduced.

## 4. Test strategy (under 150 words)

Automate 10 high-value UI test functions with Playwright: standard login, locked-out login, invalid credentials, price low-to-high sorting (checking the full list), name A-to-Z sorting, adding two items and removing one, removing an item from the cart, parameterized required-checkout-field validation, full checkout totals and confirmation, and protected-URL access after logout. Keep locators and page actions in Page Objects, use built-in waits, capture screenshots on failure, and publish an HTML or JUnit report. If supported APIs or unit tests were available, validate price/tax calculations, checkout rules, session authorization, and order creation at those layers; do not invent or call undocumented endpoints. Keep usability, responsive layout, keyboard accessibility, and exploratory checks of known-problem users manual. **Biggest remaining risk:** UI tests against a public demo cannot prove backend order integrity, tax correctness across all edge cases, or production security behavior.

## 5. A2 automation plan and traceability (initial scope: 10 automated tests)

**Scope decision:** The assignment requires at least eight automated tests and explicitly lists six required behaviors. The initial suite will contain **10 automated test functions**. The missing-first-name, missing-last-name, and missing-postal-code checks are implemented as **one parameterized test function with three data cases**, as requested. Manual test IDs remain the source of truth; automated test names begin with their corresponding TC IDs.

| Planned automated test # | Manual case ID(s) | Automated test name | Coverage / traceability note |
|---:|---|---|---|
| 1 | TC01 | `test_TC01_standard_user_logs_in` | Required: standard user login; assert Products page is visible. |
| 2 | TC02 | `test_TC02_locked_out_user_cannot_log_in` | Required: locked-out user is denied; assert error and no Products page. |
| 3 | TC03 | `test_TC03_invalid_credentials_rejected` | Additional negative-login regression. |
| 4 | TC06 | `test_TC06_sort_price_low_to_high` | Required sorting coverage: compare the **entire** displayed price list with its sorted copy, not only the first item. |
| 5 | TC08 | `test_TC08_sort_name_a_to_z` | Additional sorting regression; verify the complete product-name sequence. |
| 6 | TC10 | `test_TC10_add_two_remove_one_and_verify_cart` | Required cart coverage: add two products, remove one on Products page, assert badge transitions and remaining cart contents. |
| 7 | TC11 | `test_TC11_remove_item_from_cart` | Verify removal from the Cart page and updated cart state. |
| 8 | TC15, TC16, TC17 | `test_TC15_TC16_TC17_required_checkout_fields` | Required: one parameterized test function with three cases, leaving first name, last name, or postal code blank in turn. |
| 9 | TC19 | `test_TC19_complete_checkout_totals_and_empty_cart` | Required full checkout: assert item total, tax, total = item total + tax, confirmation, and empty cart afterwards. |
| 10 | TC21 | `test_TC21_products_url_denied_after_logout` | Required security/session check: log out, open Products URL directly, assert protected content is not accessible. |

### Manual-only or deferred cases

The following cases are **not part of the initial 10 automated test functions** and will remain manual or be considered for a later regression expansion: TC04, TC05, TC07, TC09, TC12, TC13, TC14, TC18, TC20, TC22, TC23, and TC24. TC18 remains manual until the postal-code validation rule is confirmed. TC22–TC24 require human usability, responsive-layout, or keyboard-accessibility evaluation. The broader cases TC04, TC05, TC07, TC09, TC12–TC14, and TC20 are deferred to keep the first implementation focused on the required assessment behaviors.

### Traceability rules for implementation and reporting

- Keep the manual case ID at the start of each automated test name so failures map directly to A1.
- The three required-field variants map to TC15, TC16, and TC17 even though they share one parameterized test function.
- Keep this table synchronized with actual test names in the code and with the README mapping table. Do not mark a case automated until its test is implemented and passing.
- Each automated test must be independently runnable, use configured base URL and credentials, avoid fixed sleeps, and save a screenshot on failure; generate a readable HTML or JUnit XML report.
