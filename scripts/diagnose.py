"""CI diagnostic: real Odoo state after a login attempt.

Used once to capture the ACTUAL elements Odoo 17 renders after login, so the
Page Object selectors can be corrected from evidence rather than guesswork.
Saves snapshots under ./screenshots so the CI can upload them as artifacts.
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8069")
os.makedirs("screenshots", exist_ok=True)


def main() -> int:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--ignore-certificate-errors")
    if os.environ.get("CHROME_BINARY"):
        opts.binary_location = os.environ["CHROME_BINARY"]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.implicitly_wait(5)
    lines = []
    try:
        driver.get(f"{BASE_URL}/web/login")
        time.sleep(8)
        lines.append(f"LOGIN PAGE  title={driver.title!r} url={driver.current_url}")
        lines.append("  input[name=login]    : %s" % bool(driver.find_elements(By.CSS_SELECTOR, "input[name='login']")))
        lines.append("  input[name=password] : %s" % bool(driver.find_elements(By.CSS_SELECTOR, "input[name='password']")))
        lines.append("  button[type=submit]  : %s" % bool(driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")))
        try:
            driver.find_element(By.CSS_SELECTOR, "input[name='login']").send_keys("admin")
            driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("admin")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        except Exception as exc:  # noqa: BLE001
            lines.append("  login-fill error: %s" % exc)
        time.sleep(15)
        lines.append(f"AFTER LOGIN  title={driver.title!r} url={driver.current_url}")
        for sel in (
            "button.o_menu_brand",
            "button.o_user_menu, .o_user_menu",
            "nav.o_main_navbar",
            ".o_app",
            ".o_topbar",
            "div.o_web_client",
            "input.o_searchview_input",
        ):
            lines.append("  found %-28r -> %s" % (sel, bool(driver.find_elements(By.CSS_SELECTOR, sel))))

        with open("screenshots/diagnose.html", "w", encoding="utf-8") as fh:
            fh.write(driver.page_source)
        driver.save_screenshot("screenshots/diagnose.png")
    finally:
        driver.quit()

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())