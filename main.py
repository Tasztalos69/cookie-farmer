import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv, dotenv_values

load_dotenv()


def login(driver: WebDriver):
    print("logging in...")
    username = driver.find_element(By.ID, "username")
    passw = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.CLASS_NAME, "js-login-button")

    username.send_keys(os.getenv("LOGI_USERNAME"))
    passw.send_keys(os.getenv("LOGI_PASS"))
    login_btn.click()
    time.sleep(5)
    print("logged in!")


def collect_cookies(driver: WebDriver):
    cookies = driver.find_elements(By.CSS_SELECTOR, "button[class*='CookieHunt__Button']")
    for c in cookies:
        try:
            driver.execute_script("arguments[0].setAttribute('style', 'z-index: 1000')", c)
            c.click()
        except Exception:
            pass
    return len(cookies)


def main():
    profile_dir = str(Path(__file__).resolve().parent.absolute()) + "\profile"

    # Browser setup
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    options.add_argument("--window-size=1920x1080")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')
    options.headless = True
    driver = webdriver.Chrome(options=options)
    # driver.implicitly_wait(1)
    driver.maximize_window()

    # Automation
    driver.get("https://my.logiscool.com")
    if "api" in driver.current_url:
        login(driver)

    links = ["Tanterem", "Belépés kvízbe", "Mégsem", "Új tantermi projekt", "Projekt feloldása", "Mégsem",
             "Projektjeim", "Közösség", "Projektjeim", "Projekt megosztása", "Felfedezés", "Kihívások", "Kvízek",
             "Küldetések", "Mini küldetések", "High score játékok", "Események"]

    print("Started farming cookies.")
    time.sleep(3)
    run = 1
    while True:
        cookie_count = 0
        for link in links:
            try:
                driver.find_element(By.XPATH, f"//*[text()='{link}']").click()
            except Exception:
                pass
            cookie_count += collect_cookies(driver)
        print(f"[{run}] Collected {cookie_count} cookies.")
        cookie_count = 0
        run += 1
        driver.refresh()
        time.sleep(3)


if __name__ == '__main__':
    uname = os.getenv("LOGI_USERNAME")
    passw = os.getenv("LOGI_PASS")
    if uname == "" or uname is None or passw == "" or passw is None:
        print("Login details not provided!")
        sys.exit()
    main()
