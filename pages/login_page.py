"""Login page object for the Odoo web client (/web/login)."""

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.dashboard_page import DashboardPage


class LoginPage(BasePage):
    """Encapsulates the Odoo login form.

    Odoo 17 login form: submit button is the only ``button[type=submit]`` and
    the credential fields are keyed by ``name``, so these locators are stable
    across themes/versions we target.
    """

    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='login']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORM_CARD = (By.CSS_SELECTOR, ".oe_login_form, #login, .o_login_form")
    ERROR_ALERT = (
        By.CSS_SELECTOR,
        ".oe_login_form .alert, .alert-danger, #messagebox, .o_login_form .alert",
    )

    def open(self) -> "LoginPage":
        """Navigate to the Odoo login page."""
        super().open("/web/login")
        return self

    def fill_credentials(self, username: str, password: str) -> "LoginPage":
        """Type the credentials (Odoo trusts these only on the login page)."""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def submit(self) -> DashboardPage:
        """Click Log in and hand over to the dashboard that follows."""
        self.click(self.SUBMIT_BUTTON)
        return DashboardPage(self.driver, self.base_url)

    def login(self, username: str, password: str) -> DashboardPage:
        """Complete a login flow and return the resulting dashboard page."""
        self.fill_credentials(username, password)
        return self.submit()

    def login_error_message(self) -> str:
        """Return the text of the visible credential error alert."""
        from selenium.webdriver.support import expected_conditions as EC

        element = self.wait.until(EC.visibility_of_element_located(self.ERROR_ALERT))
        return element.text.strip()