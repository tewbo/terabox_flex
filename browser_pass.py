from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from Uploader import Uploader

PROXY_HOST = 'localhost'
PROXY_PORT = 8090


def update_sign():
    print("обновление sign")
    proxy = f"{PROXY_HOST}:{PROXY_PORT}"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--proxy-server={0}".format(proxy))
    options.add_argument("--ignore-certificate-errors")

    browser = webdriver.Chrome(options=options)

    browser.get("https://www.terabox.com/example404page")
    cookies = Uploader.parseCookieFile()
    for key in cookies:
        kekw = {"name": key,
                "value": cookies[key],
                "domain": "terabox.com"}
        browser.add_cookie(kekw)
    browser.get("https://www.terabox.com/main?category=all")

    checkbox = browser.find_elements(By.CSS_SELECTOR, ".u-checkbox__input .u-checkbox__original")[-1]
    browser.execute_script("arguments[0].click();", checkbox)

    button = browser.find_element(By.XPATH, "//button[@title='Скачать']")
    browser.execute_script("arguments[0].click();", button)
    sleep(3)

    browser.quit()
    print("обновление отработало успешно")


if __name__ == "__main__":
    update_sign()
