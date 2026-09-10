"""Base Page Object that all Odoo page objects extend.

Centralises the real ERP automation concerns: WebDriver exact waits,
explicit, readable locators, and low-noise helper methods.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Shared behaviour for every page in the Odoo web client."""

    # Sensible upper bound for heavy ERP pages (Odoo renders eagerly).
    DEFAULT_TIMEOUT = 30

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=self.DEFAULT_TIMEOUT)

    # -- navigation ---------------------------------------------------------
    def open(self, path: str = "") -> "BasePage":
        """Navigate the browser to ``<base_url><path>``."""
        self.driver.get(f"{self.base_url}{path}")
        return self

    # -- lookup helpers ------------------------------------------------------
    # Every method takes a Selenium locator tuple ``(By, value)`` exactly as it
    # is declared on the page objects (e.g. ``(By.CSS_SELECTOR, "input[name=..]")``).
    def find_visible(self, locator) -> WebElement:
        """Wait for a visible element, then return it (raises TimeoutException)."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator) -> WebElement:
        """Wait for an element to exist in the DOM, then return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_present_all(self, locator) -> list[WebElement]:
        """Wait until at least one matching element exists, then return all."""
        self.wait.until(EC.presence_of_element_located(locator))
        by, value = locator
        return self.driver.find_elements(by, value)

    def find_clickable(self, locator) -> WebElement:
        """Wait for an element to be visible and enabled (clickable)."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator) -> "BasePage":
        """Wait for and click an element."""
        self.find_clickable(locator).click()
        return self

    def type_text(self, locator, text: str, clear: bool = True) -> "BasePage":
        """Wait for an input, optionally clear it, then type ``text``."""
        element = self.find_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)
        return self

    # -- state --------------------------------------------------------------
    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def is_text_visible(self, text: str) -> bool:
        """True once ``text`` appears anywhere in the page body."""
        body = self.driver.find_element("css selector", "body")
        return self.wait.until(lambda _: text in body.text)