"""E2E tests for the Odoo dashboard / application navigation."""


def test_dashboard_renders_application_chrome(login):
    login.open()
    assert login.is_dashboard_loaded()


def test_user_is_authenticated_on_dashboard(login):
    login.open()
    assert login.is_user_logged_in()


def test_apps_menu_switcher_is_present(login):
    login.open()
    assert len(login.find_present_all(login.APPS_MENU)) >= 1


def test_can_navigate_to_contacts_via_apps(login):
    contacts = login.goto_contacts()
    assert contacts.is_list_view_loaded()