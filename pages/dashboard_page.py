"""Dashboard ("Applications"/home) page object for the Odoo web client."""

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.contacts_page import ContactsPage


class DashboardPage(BasePage):
    """The post-login landing page and web-client chrome.

    Selectors below are aligned with the REAL Odoo 17 DOM (verified against a
    live instance): the top navigation bar is ``nav.o_main_navbar``, the app
    switcher button lives in ``.o_navbar_apps_menu`` and the account menu is
    ``.o_user_menu``.
    """

    # Top navigation chrome ------------------------------------------------
    APPS_MENU = (By.CSS_SELECTOR, ".o_navbar_apps_menu button.dropdown-toggle")
    USER_MENU = (By.CSS_SELECTOR, "div.o_user_menu button.dropdown-toggle, .o_user_menu button")
    MAIN_MENU = (By.CSS_SELECTOR, "nav.o_main_navbar")

    # Applications dashboard tiles (present on the home / apps board). ------
    APP_TILES = (By.CSS_SELECTOR, ".o_app")

    def open(self) -> "DashboardPage":
        """Navigate to the Odoo web client (lands on the last app / home)."""
        super().open("/web")
        return self

    def is_dashboard_loaded(self) -> bool:
        """True once the top navigation bar is present."""
        self.find_present(self.MAIN_MENU)
        return True

    def is_user_logged_in(self) -> bool:
        """True once the account/user menu is present."""
        self.find_present(self.USER_MENU)
        return True

    def wait_for_app_tiles(self) -> int:
        """Return how many application tiles the dashboard shows (home board)."""
        return len(self.find_present_all(self.APP_TILES))

    def open_app(self, name: str) -> "DashboardPage":
        """Open the app switcher dropdown and click the app named ``name``."""
        self.click(self.APPS_MENU)
        item = self.find_clickable(
            (By.XPATH, f"//a[contains(normalize-space(.), '{name}')]")
        )
        item.click()
        return self

    def goto_contacts(self) -> ContactsPage:
        """Switch to the Contacts application via the app switcher."""
        self.open_app("Contacts")
        return ContactsPage(self.driver, self.base_url)