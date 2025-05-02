"""
login_scraper.py

A script to automatically download course evaluation PDFs from JHU's evaluation system.
Uses Selenium to automate the login process and PDF downloads for specified courses.

Usage:
    python login_scraper.py --courses courses.txt
    
    where courses.txt contains one course name per line to download evaluations for.
    
    Environment variables required:
    - CURRENTUSERNAME: JHU SSO username
    - CURRENTPASSWORD: JHU SSO password
"""

import os 
from time import sleep
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse

### Parse command line arguments ###
parser = argparse.ArgumentParser(description='Download course evaluation PDFs for courses')
parser.add_argument('--courses', help='File containing courses to download on each line')
args = parser.parse_args()

### Read courses to download from file ###
with open(args.courses, "r") as f:
    COURSES_TO_DOWNLOAD = [line.strip() for line in f.readlines()]


### Load environment variables ###
load_dotenv()
usernameStr = os.getenv("CURRENTUSERNAME")
passwordStr = os.getenv("CURRENTPASSWORD")


### Start the Selenium WebDriver ###
download_dir = os.path.abspath(f"course pdfs/{args.courses.split('.')[-2]}/")

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True 
}
options = Options()
options.add_experimental_option("prefs", prefs)
browser = Chrome(options=options)


### Navigate to the home link ###
BASE_LINK = "https://asen-jhu.evaluationkit.com/Report/Public/Results?Course=&Instructor=&Search=true"
browser.get(BASE_LINK)
sleep(3) # WAIT: until the base page is loaded


### Login to JHU SSO ###

# Enter Username
sleep(3) # WAIT: until the username field is loaded
username = browser.find_element(By.ID, 'i0116')
username.send_keys(usernameStr)
nextButton = browser.find_element(By.ID, 'idSIButton9')
nextButton.click()

# Enter Password
sleep(3) # WAIT: until the password field is loaded
password = browser.find_element(By.ID, 'i0118')
password.send_keys(passwordStr)
submitButton = browser.find_element(By.ID, "idSIButton9")
submitButton.click()


### Download PDFs for a given course ###
def download_course(course_name):
    course_name = course_name.replace(" ", "+")
    link = f"https://asen-jhu.evaluationkit.com/Report/Public/Results?Course={course_name}&Instructor=&Search=true"
    browser.get(link)

    sleep(5) # WAIT: until the course search page is loaded

    while True:
        try:
            WebDriverWait(browser, 5).until(lambda d : d.find_element(By.ID, 'publicMore')) # WAIT: until the show more button is loaded
            show_more_button = browser.find_element(By.ID, 'publicMore')
            show_more_button.click()
        except:
            break
    sleep(5) # WAIT: until the the whole course search page is loaded

    # Track unique PDF buttons using their data attributes
    unique_pdf_buttons = set()
    pdf_buttons = browser.find_elements(By.CLASS_NAME, "sr-pdf")
    
    # Download each PDF
    URLS = []
    for button in pdf_buttons:
        # Get the data attributes
        id0 = button.get_attribute("data-id0")
        id1 = button.get_attribute("data-id1")
        id2 = button.get_attribute("data-id2")
        id3 = button.get_attribute("data-id3")
        
        # Create a unique identifier for this PDF
        pdf_id = f"{id0},{id1},{id2},{id3}"
        
        # Only process if we haven't seen this PDF before
        if pdf_id not in unique_pdf_buttons:
            unique_pdf_buttons.add(pdf_id)
            pdf_url = f"https://asen-jhu.evaluationkit.com/Reports/SRPdf.aspx?{pdf_id}"
            URLS.append(pdf_url)

    print(f"Found {len(unique_pdf_buttons)} unique PDFs to download")

    for url in URLS:
        browser.get(url)
        sleep(4) # WAIT: until the pdf is downloaded


sleep(5) # WAIT: until the main page is loaded
### Download PDFs for each course ###
for course in COURSES_TO_DOWNLOAD:
    download_course(course)


### TODO ###
# remove sleeps and instead figure out how to wait properly with condition checks
# - keep track of number of downloads and only stop once it matches the number of pdfs
# - utilize WebDriverWait
# error handling - if error, try again
# - if especially on login
# - failed links or just too slow
# add diagnostics/results of run
