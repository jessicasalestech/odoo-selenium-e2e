"""Browserless coherence checks for the Page Object layer.

These run WITHOUT a browser or an Odoo instance, so they are the tests we can
run on any machine without Docker. They guard the framework itself: every page
must declare its published locators with a valid Selenium ``By`` argument so the
suite never collapses to import/attribute errors under the real E2E run.
"""

from selenium.webdriver.common.by import By

import pytest

import pages
from pages.base import BasePage
from pages.contacts_page import ContactsPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.unit

# Locator attributes that begin with a capital letter (by Selenium convention).
_ALLOWED_BY = {By.ID, By.CSS_SELECTOR, By.XPATH, By.NAME, By.CLASS_NAME, By.LINK_TEXT}


def _locator_attributes(cls):
    return {
        name: value
        for name, value in vars(cls).items()
        if name.isupper() and isinstance(value, tuple) and len(value) == 2
    }


def test_all_pages_derive_from_base_page():
    for klass in (LoginPage, DashboardPage, ContactsPage):
        assert issubclass(klass, BasePage), f"{klass.__name__} must extend BasePage"


def test_login_page_publishes_working_locators():
    locators = _locator_attributes(LoginPage)
    assert {"USERNAME_INPUT", "PASSWORD_INPUT", "SUBMIT_BUTTON", "ERROR_ALERT"} <= set(locators)
    for by_, _value in locators.values():
        assert by_ in _ALLOWED_BY


def test_dashboard_page_publishes_working_locators():
    locators = _locator_attributes(DashboardPage)
    assert {"APPS_MENU", "USER_MENU", "MAIN_MENU", "APP_TILES"} <= set(locators)
    for by_, _value in locators.values():
        assert by_ in _ALLOWED_BY


def test_contacts_page_publishes_working_locators():
    locators = _locator_attributes(ContactsPage)
    assert {"SEARCH_INPUT", "NEW_BUTTON", "NAME_INPUT", "SAVE_BUTTON", "ACTION_DROPDOWN"} <= set(
        locators
    )
    for by_, _value in locators.values():
        assert by_ in _ALLOWED_BY


def test_page_exports_pyramid():
    for name in ("BasePage", "LoginPage", "DashboardPage", "ContactsPage"):
        assert hasattr(pages, name), f"pages package should export {name}"


def test_default_base_url_matches_docker_compose():
    # The local-default URL must agree with the docker-compose published port.
    from conftest import BASE_URL

    assert BASE_URL == "http://localhost:8069"


def test_credentials_constant_defaults_are_test_only():
    from conftest import ADMIN_USER, ADMIN_PASSWORD

    assert ADMIN_USER == "admin"
    assert ADMIN_PASSWORD == "admin"