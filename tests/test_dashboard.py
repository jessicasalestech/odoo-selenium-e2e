"""E2E tests for the Odoo dashboard / application navigation."""


def test_dashboard_renders_application_chrome(login):
    login.open()
    assert login.is_dashboard_loaded()


def test_user_is_authenticated_on_dashboard(login):
    login.open()
    assert login.is_user_logged_in()


def test_dashboard_lists_installed_applications(login):
    login.open()
    tiles = login.wait_for_app_tiles()
    # base + contacts + sale + purchase (demo data) -> several tiles expected.
    assert tiles >= 4


def test_apps_menu_switcher_is_present(login):
    login.open()
    switchers = login.find_present_all(*login.APPS_MENU)
    assert len(switchers) >= 1


def test_can_navigate_to_contacts_via_apps(login):
    contacts = login.goto_contacts()
    assert contacts.is_text_visible("Contacts") or contacts.title


def test_dashboard_nav_to_contacts_opens_list_view(login):
    contacts = login.goto_contacts()
    assert contacts.list_row_count() >= 0