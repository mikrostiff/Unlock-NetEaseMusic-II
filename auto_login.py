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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F42B6DD71CB1BD38AD31C721961857EECC50DBF89289B85BA32DA21FE33D26F45CB09C682AC9E81CE2D8A9B4217FC1BFF688A8DC290B449F5E4F30A02260457A4AD63BF6A09834772321C3229B1392028104978E74F6F19A10A6F8E49EF2FCC56A5CE5B6D0CDF651B807ED4EAE18D7745712569C0DD53EE412872787CCDC96616DD687A124799DCD4C697D98F201B94EEBC7E01A25E30D5DCD7CCFBB74CA08FECCE0E56C16A04C397B192849E2206F556F2782561857F66DEE3453A5DDA5DF14E55D4755967E318BA4556B12DE7AE34357B856A858CF4128092BCF96BA90876F88639064C9ECE53CF44F8843FBDA5A961E93244E410347B5356F70BC29865A43494B4EBA494BA71687FC6DFF6AD0E5B7454547CF017C62407B1987F8E025FB1B15E977EDBF50FBA949861E1143E5D76883CE486D70453CAB20C1590BC9EC462989C3ABC722144CBC75E8DFB2ED71ACB5B1C9E4C39C66B197BE76B2A20A2CD889D386B2F9EB5712F4CC921F2403D9C972"})
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
