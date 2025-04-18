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
import requests
from urllib.parse import quote, unquote


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
WebDriverWait(browser, 20).until(lambda d : d.find_element(By.ID, 'i0118'))
password = browser.find_element(By.ID, 'i0118')
password.send_keys(passwordStr)

WebDriverWait(browser, 10).until(lambda d : d.find_element(By.ID, 'idA_PWD_ForgotPassword'))
submitButton = browser.find_element(By.ID, "idSIButton9")
submitButton.click()

sleep(10)

browser.get(LINK)

# TODO SCRAPE THE PAGE

# Find all PDF download buttons
pdf_buttons = browser.find_elements(By.CLASS_NAME, "sr-pdf")
print(len(pdf_buttons))

# Create a session for downloading PDFs
session = requests.Session()
cookies = browser.get_cookies()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Download each PDF
for i, button in enumerate(pdf_buttons, start=1):
    # Get the data attributes
    id0 = button.get_attribute("data-id0")
    id1 = button.get_attribute("data-id1")
    id2 = button.get_attribute("data-id2")
    id3 = button.get_attribute("data-id3")

    # Clean/Decode the values
    id1 = unquote(id1)
    id2 = unquote(id2)
    id3 = unquote(id3)

    # Build the URL
    pdf_url = f"{id0},{id1},{id2},{id3}"
    pdf_url = "https://asen-jhu.evaluationkit.com/Reports/SRPdf.aspx?" + quote(pdf_url, safe="()!.,")
    print(f"[+] Downloading PDF #{i} from {pdf_url}")

#     # Download and save
    # pdf_resp = session.get(pdf_url)
    # with open(f"report_{i}.pdf", "wb") as f:
    #     f.write(pdf_resp.content)

print("✅ All PDFs downloaded!")

sleep(10)
