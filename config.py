
import os

# Application configuration
BASE_URL = os.getenv(
    "SAUCEDEMO_BASE_URL",
    "https://www.saucedemo.com"
)

# Test users
STANDARD_USER = os.getenv(
    "SAUCEDEMO_STANDARD_USER",
    "standard_user"
)

LOCKED_OUT_USER = os.getenv(
    "SAUCEDEMO_LOCKED_OUT_USER",
    "locked_out_user"
)

PASSWORD = os.getenv(
    "SAUCEDEMO_PASSWORD",
    "secret_sauce"
)
