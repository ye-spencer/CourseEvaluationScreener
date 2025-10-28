"""
login_scraper.py

A script to automatically download course evaluation PDFs from JHU's evaluation system.
Uses Selenium to automate the login process and PDF downloads for specified courses.

Usage:
    python login_scraper.py --courses <filename.txt>
    
    where <filename.txt> contains one course name per line to download evaluations for.
    
    Environment variables required:
    - CURRENTJHUSSOUSERNAME: JHU SSO username
    - CURRENTJHUSSOPASSWORD: JHU SSO password
"""

import os 
import time
import glob
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse

def wait_for_downloads(download_dir: str, expected_count: int, timeout: int = 180) -> bool:
    """
    Wait until all evaluation report PDFs are downloaded

    Args:
        download_dir (str): Directory to store downloaded PDFs
        expected_count (str): # of expected PDFs
        timeout (int): Maximum time to wait until download completes
    """
    os.makedirs(download_dir, exist_ok=True)
    start = time.time()
    while time.time() - start < timeout:
        tmp = glob.glob(os.path.join(download_dir, "*.crdownload"))
        pdfs = glob.glob(os.path.join(download_dir, "*.pdf"))
        if not tmp and len(pdfs) >= expected_count:
            return True
        time.sleep(1)
    return False


def expand_all_results(wait: WebDriverWait):
    """
    Use WebDriverWait to keep click show more button until no more button shows up

    Args:
        wait (WebDriverWait): WebDriverWait instance
    """
    while True:
        try:
            curr = len(browser.find_elements(By.CLASS_NAME, "sr-pdf")) # current number of PDF button
            btn = wait.until(EC.element_to_be_clickable((By.ID, "publicMore"))) # WAIT: until PDF button is clickable
            btn.click()
            WebDriverWait(browser, 10).until( lambda d: len(d.find_elements(By.CLASS_NAME, "sr-pdf")) > curr ) # WAIT: until pdf button increases (max wait: 10 seconds)
        except :
            break

def download_course(course_name: str) -> None:
    """
    Download all evaluation report PDFs for a given JHU course.

    Args:
        course_name (str): The exact course name (e.g., "Computer Vision")
        Spaces are automatically replaced with '+' to fit URL encoding.
    """
    course_name_origin = course_name
    course_name = course_name.replace(" ", "+")  # replace space with +, allowing encoding into URL
    link = f"https://asen-jhu.evaluationkit.com/Report/Public/Results?Course={course_name}&Instructor=&Search=true"
    browser.get(link)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")      # WAIT: until login page is loaded

    ### Load all pages of search result ###
    expand_all_results(wait)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")      # WAIT: until all search page is loaded

    # Track unique PDF buttons using their data attributes
    unique_pdf_buttons = set()
    pdf_buttons = browser.find_elements(By.CLASS_NAME, "sr-pdf")
    
    # Download each PDF
    URLS = []
    for button in pdf_buttons:
        container = button.find_element(By.XPATH, ".//ancestor::div[contains(@class,'row')][1]")
        h2 = container.find_element(By.CSS_SELECTOR, "div.sr-dataitem-info h2")
        txt = h2.text.strip()
        if (txt != course_name_origin):
            continue
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
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete") # WAIT: until the pdf is loaded

    ### Check whether download is successfully done ###
    done = wait_for_downloads(download_dir, expected_count=len(URLS), timeout=180)
    print(f"[{course_name_origin}] downloads {'DONE' if done else 'TIMEOUT'}")

##### MAIN CODE #####
DOWNLOAD_DIRECTORY = None

### Parse command line arguments ###
parser = argparse.ArgumentParser(description='Download course evaluation PDFs for courses')
parser.add_argument('--courses', help='File containing courses to download on each line')
args = parser.parse_args()
if not args.courses or not os.path.exists(args.courses):
    raise FileNotFoundError(f"--courses not found: {args.courses}") # raise error if courses argument is invalid

### Read courses to download from file ###
with open(args.courses, "r") as f:
    COURSES_TO_DOWNLOAD = [line.strip() for line in f.readlines()]

### Load environment variables ###
load_dotenv()
usernameStr = os.getenv("CURRENTJHUSSOUSERNAME")
passwordStr = os.getenv("CURRENTJHUSSOPASSWORD")
if not usernameStr or not passwordStr:
    raise EnvironmentError("CURRENTJHUSSOUSERNAME/CURRENTJHUSSOPASSWORD is empty") # raise error if env is empty


### Start the Selenium WebDriver ###
download_dir = os.path.abspath(f"course pdfs/{args.courses.split('.')[-2]}/") # set directory for downloaded pdfs

### Setting Chrome Download Options ###
prefs = {
    "download.default_directory": download_dir,  # setting download directory
    "download.prompt_for_download": False,       # automate the download without asking
    "download.directory_upgrade": True,          # give access to chrome to modify download directory
    "plugins.always_open_pdf_externally": True   # disallow opening pdf with internal viewer
}
options = Options()
options.add_experimental_option("prefs", prefs)  
browser = Chrome(options=options)                # applying prefs to Chrome
wait = WebDriverWait(browser, timeout=20)        # WebDriverWait instance for waiting 20 seconds max until given condition is met

### Navigate to the home link ###
BASE_LINK = "https://asen-jhu.evaluationkit.com/Report/Public/Results?Course=&Instructor=&Search=true"
browser.get(BASE_LINK)
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")        # WAIT: until webpage is loaded
                                                                                          # by executing JS script, check readyState == complete

### Login to JHU SSO ###
# Enter Username
wait.until(EC.visibility_of_element_located((By.ID, "i0116"))).send_keys(usernameStr)     # WAIT: until ID page is visible
wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()                    # WAIT: until ID button is clickable

# Enter Password
wait.until(EC.visibility_of_element_located((By.ID, "i0118"))).send_keys(passwordStr)     # WAIT: until password page is visible
wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()                    # WAIT: until password button is clickable

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")        # WAIT: until the main page is loaded
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


