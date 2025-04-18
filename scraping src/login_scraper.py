import os 
from time import sleep
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

COURSES_TO_DOWNLOAD = ["functional programming", "operating systems"]

### Load environment variables ###
load_dotenv()
usernameStr = os.getenv("CURRENTUSERNAME")
passwordStr = os.getenv("CURRENTPASSWORD")

### Start the Selenium WebDriver and navigate to the home link ###
browser = Chrome()
BASE_LINK = "https://asen-jhu.evaluationkit.com/Report/Public/Results?Course=&Instructor=&Search=true"
browser.get(BASE_LINK)

sleep(3)


### Login to JHU SSO ###

# Wait for and get username field
WebDriverWait(browser, 5).until(lambda d : d.find_element(By.ID, 'i0116'))
username = browser.find_element(By.ID, 'i0116')
username.send_keys(usernameStr)

# Click next button
nextButton = browser.find_element(By.ID, 'idSIButton9')
nextButton.click()

# Wait for and get password field
WebDriverWait(browser, 5).until(lambda d : d.find_element(By.ID, 'i0118'))
password = browser.find_element(By.ID, 'i0118')
password.send_keys(passwordStr)

# Click submit button
WebDriverWait(browser, 5).until(lambda d : d.find_element(By.ID, 'idA_PWD_ForgotPassword'))
submitButton = browser.find_element(By.ID, "idSIButton9")
submitButton.click()


### Download PDFs for a given course ###
def download_course(course_name):
    course_name = course_name.replace(" ", "+")
    link = f"https://asen-jhu.evaluationkit.com/Report/Public/Results?Course={course_name}&Instructor=&Search=true"

    browser.get(link)

    sleep(10) # WAIT: until the course search page is loaded

    while True:
        try:
            WebDriverWait(browser, 5).until(lambda d : d.find_element(By.ID, 'publicMore')) # WAIT: until the show more button is loaded
            show_more_button = browser.find_element(By.ID, 'publicMore')
            show_more_button.click()
        except:
            break
    print("Clicked show more as many times as possible")
    sleep(10) # WAIT: until the the whole course search page is loaded

    pdf_buttons = []
    pdf_buttons = browser.find_elements(By.CLASS_NAME, "sr-pdf")
    print(len(pdf_buttons))
    
    # Download each PDF
    URLS = []
    for i, button in enumerate(pdf_buttons, start=1):
        # Get the data attributes
        id0 = button.get_attribute("data-id0")
        id1 = button.get_attribute("data-id1")
        id2 = button.get_attribute("data-id2")
        id3 = button.get_attribute("data-id3")

        # Build the URL directly without unnecessary encoding/decoding
        pdf_url = f"https://asen-jhu.evaluationkit.com/Reports/SRPdf.aspx?{id0},{id1},{id2},{id3}"
        URLS.append(pdf_url)


    for url in URLS:
        browser.get(url)
        sleep(10) # WAIT: until the pdf is downloaded


sleep(5) # WAIT: until the main page is loaded
### Download PDFs for each course ###
for course in COURSES_TO_DOWNLOAD:
    download_course(course)


# TODO
# remove sleeps and instead figure out how to wait properly with condition checks
# - keep track of number of downloads and only stop once it matches the number of pdfs
# - utilize 
# error handling - if error, try again
# move pdf downloads to a custom folder
