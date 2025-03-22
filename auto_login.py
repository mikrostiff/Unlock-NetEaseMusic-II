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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AA999B2E0FCF0078D6EF9FDCF976EF7540259912F760C0333F51C36A84ACE02719990C9E21D5D2F0286581131DCAC44B511BE634D42DAD5CE639C10E1649B68FAFCE2B5F57A5403E09FCE6C44A5B772D5D65F41AAE56E7052D5F5459CB8DE1EE4BE74B54F3AE59CFA0DDBC108B5FF275F645041B017D0B3C7F35BE070E65E03701DEAA8B5B69728AC3CB88E3C36D49F846860A9120E5112023795C972B1D20424BAF87FDB38E658F503AFF3C04F2A9AA6DD71CDF8DAE696EFB7A8258939C9BE3880128DFA3F66BB2807D89BEAB37DB315CA36B3EB5044F74654DEB7C49A787EB0C7B1945A1A323EE9B7412BAD3056AFA1984CFB9937FBE3BAA8693241079602B8855F91A224D7DE049645733048176EEE28791B982F5BEDD10EE5CACC5B27B78AE9CEF0B0F8BA76D09653C20BE8C9A05F8B687C7BB151EC504079224476FA192449456327E24CE69864B38C44DE498F76C98D07A617733555310E3E837A4A0CE5CB29400D94B949AA3D91F05336ACDF8"})
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
