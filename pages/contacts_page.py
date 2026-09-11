"""Contacts application page object.

Exercises a real ERP CRUD flow: create a partner, find it, edit it, delete it.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base import BasePage


class ContactsPage(BasePage):
    """List/form views of Odoo's Contacts (partners) application."""

    # List view chrome ------------------------------------------------------
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.o_searchview_input")
    NEW_BUTTON = (
        By.CSS_SELECTOR,
        "button[name='new'], button[data-title='New'], .o_list_button_add",
    )
    LIST_ROWS = (By.CSS_SELECTOR, ".o_kanban_record, tr.o_data_row")

    # Form view chrome ------------------------------------------------------
    NAME_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    EMAIL_INPUT = (
        By.CSS_SELECTOR,
        "input[name='email_formatted'], input[name='email'], input[name='email_normalized']",
    )
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.o_form_button_save")
    EDIT_BUTTON = (By.CSS_SELECTOR, "button.o_form_button_edit")
    DECORATION_TITLE = (By.CSS_SELECTOR, ".oe_title h1, .o_form_sheet h1, .breadcrumb")

    # Delete-flow actions ---------------------------------------------------
    ACTION_DROPDOWN = (By.CSS_SELECTOR, "button.o_form_button_action")
    DELETE_ITEM = (
        By.CSS_SELECTOR,
        ".o-dropdown-menu a[data-name='Delete'], .o-dropdown-menu .o_menu_item[data-name='Delete']",
    )

    # -- navigation ----------------------------------------------------------
    def open(self) -> "ContactsPage":
        super().open("/web#cids=1&menu_id=0&action=contacts.contacts_list_action")
        return self

    def is_list_view_loaded(self) -> bool:
        """True once the Contacts list view (search bar) is rendered."""
        self.find_visible(self.SEARCH_INPUT)
        return True

    # -- list view -----------------------------------------------------------
    def search(self, term: str) -> "ContactsPage":
        """Type into the search box and commit the search."""
        box = self.find_visible(self.SEARCH_INPUT)
        box.clear()
        box.send_keys(term)
        box.send_keys(Keys.ENTER)
        return self

    def list_row_count(self) -> int:
        return len(self.find_present_all(self.LIST_ROWS))

    def click_first_row(self) -> "ContactsPage":
        rows = self.find_present_all(self.LIST_ROWS)
        rows[0].click()
        return self

    # -- form view -----------------------------------------------------------
    def create_contact(self, name: str, email: str = "") -> "ContactsPage":
        """Open New, fill the form and save."""
        self.click(self.NEW_BUTTON)
        self.type_text(self.NAME_INPUT, name)
        if email:
            # Email field is optional; ignore if it is not editable on screen.
            try:
                box = self.find_visible(self.EMAIL_INPUT)
                box.clear()
                box.send_keys(email)
            except Exception:
                pass
        self.click(self.SAVE_BUTTON)
        return self

    def update_name(self, name: str) -> "ContactsPage":
        """From a form, edit the name field and save."""
        self.click(self.EDIT_BUTTON)
        self.type_text(self.NAME_INPUT, name)
        self.click(self.SAVE_BUTTON)
        return self

    def delete_current(self) -> "ContactsPage":
        """Open the action dropdown and choose Delete."""
        self.click(self.ACTION_DROPDOWN)
        self.click(self.DELETE_ITEM)
        return self

    # -- assertions helpers ---------------------------------------------------
    def has_record(self, name: str) -> bool:
        """True if any list row carries the given partner name."""
        from selenium.webdriver.support import expected_conditions as EC

        try:
            self.wait.until(
                lambda d: any(name in row.text for row in d.find_elements(*self.LIST_ROWS))
            )
            return True
        except Exception:
            return False