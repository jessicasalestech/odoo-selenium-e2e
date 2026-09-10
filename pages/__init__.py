"""Page Object Model package for the Odoo ERP Selenium E2E suite."""

from pages.base import BasePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.contacts_page import ContactsPage

__all__ = ["BasePage", "LoginPage", "DashboardPage", "ContactsPage"]