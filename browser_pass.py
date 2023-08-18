from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from Uploader import Uploader

PROXY_HOST = 'localhost'
PROXY_PORT = 8090
SLEEP_TIME = 3


def update_sign():
    print("Running browser...")
    proxy = f"{PROXY_HOST}:{PROXY_PORT}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--proxy-server={0}".format(proxy))
    options.add_argument("--ignore-certificate-errors")

    browser = webdriver.Chrome(options=options)

    browser.get("https://www.terabox.com/example404page")
    cookies = Uploader.parse_cookie_file()
    for key in cookies:
        kekw = {"name": key,
                "value": cookies[key]
                }
        browser.add_cookie(kekw)
    browser.get("https://www.terabox.com/main?category=all")

    checkbox = browser.find_elements(By.CLASS_NAME, "u-checkbox__original")[-1]
    browser.execute_script("arguments[0].click();", checkbox)

    try:
        button = browser.find_element(By.XPATH, "//button[@title='Скачать']")
    except:
        button = browser.find_element(By.XPATH, "//button[@title='Download']")
    browser.execute_script("arguments[0].click();", button)
    sleep(SLEEP_TIME)

    browser.quit()
    print("Sign updating was completed successful.")


if __name__ == "__main__":
    update_sign()
