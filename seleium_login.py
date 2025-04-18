import os 
import sys
import datetime
import argparse
from time import sleep
from dateutil import parser
from getpass import getpass
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


load_dotenv()

# Build-in login credentials
usernameStr = os.getenv("CURRENTUSERNAME")
passwordStr = os.getenv("CURRENTPASSWORD")

print(usernameStr)
print(passwordStr)

LINK = "https://asen-jhu.evaluationkit.com/Report/Public/Results?Course=functional+programming&Instructor=&Search=true"

# Start the Selenium WebDriver
browser = Chrome()
browser.get(LINK)

sleep(3)

# signInButton = browser.find_element(By.ID, "linkSignIn")
# signInButton.click()

# Wait for and get username field
WebDriverWait(browser, 10).until(lambda d : d.find_element(By.ID, 'i0116'))
username = browser.find_element(By.ID, 'i0116')
username.send_keys(usernameStr)

nextButton = browser.find_element(By.ID, 'idSIButton9')
nextButton.click()

# Wait for and get password field
WebDriverWait(browser, 10).until(lambda d : d.find_element(By.ID, 'i0118'))
password = browser.find_element(By.ID, 'i0118')
password.send_keys(passwordStr)

WebDriverWait(browser, 10).until(lambda d : d.find_element(By.ID, 'idA_PWD_ForgotPassword'))
submitButton = browser.find_element(By.ID, "idSIButton9")
submitButton.click()

sleep(10)

browser.get(LINK)

# TODO SCRAPE THE PAGE

sleep(10)

print("Successfully logged in")