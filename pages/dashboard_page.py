"""Dashboard ("Applications"/home) page object for the Odoo web client."""

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.contacts_page import ContactsPage


class DashboardPage(BasePage):
    """The post-login landing page and the Applications/home dashboard.

    In Odoo the home dashboard renders every installed app as a tile. The
    top application menu (four-square switcher) is keyed by ``o_menu_brand``
    and the account menu by ``o_user_menu``.
    """

    # Top navigation chrome ------------------------------------------------
    APPS_MENU = (By.CSS_SELECTOR, "button.o_menu_brand")
    USER_MENU = (By.CSS_SELECTOR, "button.o_user_menu, .o_user_menu")
    MAIN_MENU = (By.CSS_SELECTOR, ".o_topbar .breadcrumb, .o_menu_brand, nav.o_main_navbar")

    # Applications dashboard tiles ------------------------------------------
    APP_TILES = (By.CSS_SELECTOR, ".o_app")
    CONTACTS_TILE = (By.CSS_SELECTOR, ".o_app[data-menu-xmlid*='contacts'], a.o_app[href*='contacts']")

    def open(self) -> "DashboardPage":
        """Navigate straight to the Odoo home/dashboard."""
        super().open("/web")
        return self

    def is_dashboard_loaded(self) -> bool:
        """True once the top application chrome is present."""
        self.find_present(self.APPS_MENU)
        return True

    def is_user_logged_in(self) -> bool:
        """True once the account/user menu is present."""
        self.find_present(self.USER_MENU)
        return True

    def wait_for_app_tiles(self) -> int:
        """Return how many application tiles the dashboard shows."""
        return len(self.find_present_all(self.APP_TILES))

    def open_apps_menu(self) -> "DashboardPage":
        """Open the application switcher menu, if present."""
        if self.find_present_all(self.APPS_MENU):
            self.click(self.APPS_MENU)
        return self

    def goto_contacts(self) -> ContactsPage:
        """Click the Contacts application tile."""
        self.click(self.CONTACTS_TILE)
        return ContactsPage(self.driver, self.base_url)