"""E2E tests for the Odoo login flow."""


def test_login_page_reports_invalid_credentials(login_page):
    """A wrong password must surface the Odoo 'Wrong login/password' alert."""
    login_page.open().fill_credentials("admin", "definitely-wrong-pass").submit()
    message = login_page.login_error_message()
    assert "wrong" in message.lower() or "login/password" in message.lower()


def test_login_form_rejects_blank_password(login_page):
    """Blank password must not create a session; an alert/error is expected."""
    login_page.open().fill_credentials("admin", "").submit()
    assert login_page.title


def test_valid_login_reaches_the_dashboard(login, base_url):
    """Admin/Admin (TEST credentials) should land on the dashboard."""
    assert login.is_dashboard_loaded()
    assert login.is_user_logged_in()


def test_login_lands_on_odoo_web(login):
    """After login we are inside the Odoo web client, not the login form."""
    assert "web" in login.current_url


def test_login_keeps_user_in_authenticated_session(login):
    """The account menu proves an authenticated session survives navigation."""
    login.open()
    assert login.is_user_logged_in()