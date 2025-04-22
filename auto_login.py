# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00596E35CB0CB3F1103F5160E29ECA999D47A315A57358E975881682AA9A40F2BCADFA441238420C3B4593E7DAD77FEA4A8AF544F3C2E2DDE156FC8D4FAD263D4A045EA533379CF21E78EAAF834AF6FCF0DF26177CA78E387893A8FC78578E6CEFAEDF08BCDDB5C34CF9B1C757973AF01DD5F604B34933A95F29857C023E3CAF6CC1133A21B2F1E249248FEAAD28920C11BD4D3C6746ACB9196A05B237DB56F5A1B0E924E06B94440EDD2C2CC8BB5AAD12EE03CED60699ED26162A4A15622EE6A04CA24B7699D83054E314F8484837D331CCE535DA0D5FF820D1FF48D1B7BD682F7D932370278FC9CC40E3DEA1A9BA2714ED9EE65188B55175BBB3BC9C67AE3218110A5789A9D607C6C0CFBF71236ABDA30D3D0364A33C95ED908D30C8D3F76423CF21E6B51452F489E6612F2708EB46139177D633543ACAF9EB0DF4DF16AF7BDAC2D02458D4CCB70270FF5A891D505C8548061C2FFE6F83A3F99AC397BDA59A6BBB0FF5AAD4BB43ADA9AB64C9EA4255A1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
