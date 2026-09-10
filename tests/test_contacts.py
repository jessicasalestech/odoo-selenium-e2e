"""E2E tests for the Odoo Contacts application (real ERP CRUD)."""

import uuid

from pages.dashboard_page import DashboardPage


def _brand() -> str:
    """Unique contact name so parallel runs never collide."""
    return f"QA E2E Contact {uuid.uuid4().hex[:8]}"


def test_contacts_opens_from_dashboard(contacts):
    assert contacts.is_text_visible("Contacts") or contacts.title


def test_contacts_list_is_not_empty_with_demo_data(contacts):
    # With --without-demo=0 there are demo partners seeded by Odoo.
    assert contacts.list_row_count() >= 1


def test_create_contact(contacts):
    brand = _brand()
    contacts.search("")
    contacts.create_contact(brand, f"{brand.lower().replace(' ', '')}@example.com")
    # Back on the list, our new record must be findable.
    contacts.search(brand)
    assert contacts.has_record(brand)


def test_search_returns_created_contact(contacts):
    brand = _brand()
    contacts.search("")
    contacts.create_contact(brand)
    contacts.search(brand)
    assert contacts.list_row_count() >= 1
    assert contacts.has_record(brand)


def test_edit_contact_name(contacts):
    brand = _brand()
    renamed = f"{brand} (edited)"
    contacts.search("")
    contacts.create_contact(brand)
    contacts.search(brand)
    contacts.click_first_row()
    contacts.update_name(renamed)
    assert contacts.is_text_visible(renamed) or contacts.has_record(renamed)


def test_delete_created_contact(contacts):
    brand = _brand()
    contacts.search("")
    contacts.create_contact(brand)
    contacts.search(brand)
    assert contacts.has_record(brand)
    contacts.click_first_row()
    contacts.delete_current()
    # Optionally confirm via the search that the record no longer surfaces
    # in the same way (skip brittle toast assertions; the delete dialog is
    # confirmed before the row is removed).
    assert not contacts.has_record(brand)


def test_contacts_support_search_of_demo_customers(contacts):
    contacts.search("Azure")
    assert contacts.list_row_count() >= 1