
import os
from fake_useragent import UserAgent
from selenium import webdriver
import random
import time


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# setting up proxies and chrome options here
proxy_list = [
    {'http': 'http://35.233.162.87:3100'},
    {'http': 'http://174.138.184.82:37725'},
    {'http': 'http://204.2.218.145:8080'},
    {'http': 'http://88.99.234.110:2021'},
]

random.shuffle(proxy_list)

# get selenium driver
def get_driver2():
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    #from selenium.webdriver.chrome.service import Service

    ua = UserAgent()
    userAgent = ua.random

    #proxy_server = utilities.get_random_proxy()
    #print("------*****-----\n\n\n",proxy_server,"\n\n\n------*****-----")

    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.exclude_switches = ["enable_automation"]
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={userAgent}')
    # options.add_argument('--proxy-server=%s' % proxy_server)
    # options.add_argument(f'--proxy-server={proxy_server}')
    options.add_argument('--ignore-certificate-errors')

    if os.name == "nt":
        print("YES I'M running from NT ENV.....")
        return webdriver.Chrome(options=options)
    elif os.name == "posix":
        print("YES I'M running from POSIX ENV.....")
        #from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome('/home/root/chromedriver',options=options)

# get selenium driver
def get_driver():
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    ua = UserAgent()
    userAgent = ua.random

    #proxy_server = utilities.get_random_proxy()

    options = Options()
    # options.add_argument('--headless')
    options.add_argument("disable-infobars")
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument(f'--proxy-server={proxy_server}')
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument('--ignore-certificate-errors')

    if os.name == "nt":
        print("YES I'M running from NT ENV.....")
        return webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    elif os.name == "posix":
        print("YES I'M running from POSIX ENV.....")
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# step 3.
def platform_login(driver=None):
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(100)

    # finding input username field
    findInputField = driver.find_element(By.CSS_SELECTOR, 'input[name="text"]')
    findInputField.send_keys('mirzaal02254292')
    time.sleep(5)

    # clicking on next button
    clickNextButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]')))
    clickNextButton.click()
    time.sleep(5)

    # finding input password field
    findPasswordField = WebDriverWait(driver, 600).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    findPasswordField.send_keys('faizan..12')
    time.sleep(5)

    # clicking on login button
    clickNextButton = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Log in")]')))
    clickNextButton.click()
    time.sleep(10)