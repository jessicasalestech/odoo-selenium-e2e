"""Shared pytest fixtures and a failure-screenshot hook.

Design notes
------------
* ``driver`` is MODULE scoped: one headless Chrome is reused across all tests
  in a single module, which matches the "log in once per module" goal and
  keeps ERP (heavy) page loads from being paid repeatedly.
* ``login`` is MODULE scoped and yields a ready-to-use dashboard page, so the
  Contacts module logs in exactly once.
* Any test failure triggers a screenshot + HTML snapshot under ``./screenshots``
  (gitignored) to aid debugging of E2E runs.
"""

from __future__ import annotations

import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8069")
ADMIN_USER = os.environ.get("ODOO_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ODOO_PASSWORD", "admin")


def _chrome_options() -> Options:
    opts = Options()
    # --headless=new is required on CI runners (no display server).
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")       # required on GitHub Actions
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--start-maximized")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    if os.environ.get("CHROME_BINARY"):
        opts.binary_location = os.environ["CHROME_BINARY"]
    return opts


@pytest.fixture(scope="session")
def base_url() -> str:
    """The Odoo web base URL (override with BASE_URL or --base-url)."""
    return BASE_URL


@pytest.fixture(scope="module")
def driver():
    """One headless Chrome per test module."""
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=_chrome_options())
    browser.implicitly_wait(3)
    yield browser
    browser.quit()


@pytest.fixture()
def login_page(driver, base_url) -> LoginPage:
    return LoginPage(driver, base_url)


@pytest.fixture(scope="module")
def login(driver, base_url) -> DashboardPage:
    """Log into Odoo once per module as the TEST administrator."""
    login_form = LoginPage(driver, base_url).open()
    dashboard = login_form.login(ADMIN_USER, ADMIN_PASSWORD)
    dashboard.is_dashboard_loaded()
    return dashboard


@pytest.fixture()
def contacts(driver, base_url, login) -> "ContactsPage":  # noqa: F821
    from pages.dashboard_page import DashboardPage
    from pages.contacts_page import ContactsPage

    DashboardPage(driver, base_url).open()
    return login.goto_contacts()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot + page source whenever a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = _current_driver(item)
        if driver is None:
            return
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        short = item.name.replace("/", "_").replace(" ", "_")[:60]
        for ext in ("png", "html"):
            try:
                os.makedirs("screenshots", exist_ok=True)
                target = os.path.join("screenshots", f"{short}_{stamp}.{ext}")
                if ext == "png":
                    driver.save_screenshot(target)
                else:
                    with open(target, "w", encoding="utf-8") as fh:
                        fh.write(driver.page_source)
            except Exception:
                pass


def _current_driver(item):
    try:
        return item.funcargs["driver"]
    except Exception:
        return None