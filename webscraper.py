import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from browser_option import option_configure
import psutil
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(accEmail, accPassword):
    browser.get('https://www.warframe.com/login')
    time.sleep(1)

    # check if you are already logged in
    if browser.current_url != 'https://www.warframe.com/login':
        print("Already logged in. Attempting to log out. . .")
        try:
            if not headlessOn:
                # hover over username to show log out button
                hover_element = browser.find_element(By.XPATH, '//*[@id="header"]/div/div[3]/div[2]/div/div')
                hover = ActionChains(browser).move_to_element(hover_element)
                hover.perform()
            else:
                browser.find_element(By.XPATH, '//*[@id="header"]/div/div[3]/div[2]/div/div').click()
            time.sleep(0.5)
            # clicks log out button
            browser.find_element(By.XPATH, '//*[@id="header"]/div/div[7]/div[3]/a[4]/span').click()
            time.sleep(0.5)
            browser.get('https://www.warframe.com/login')
            print("Success!")
        except:
            print('Error while logging out to attempt log-in')

    # # clicks on login button
    # browser.find_element('class name', 'loginLink').click()

    # enters email address
    email = browser.find_element(By.XPATH, '//*[@id="email-login"]/input')
    email.send_keys(accEmail)

    # enters password
    password = browser.find_element(
        By.XPATH, '//*[@id="password-login"]/input')
    password.send_keys(accPassword)

    time.sleep(0.25)
    login_button = browser.find_element(By.XPATH, '//*[@id="submit-login"]/button/div/input')

    # clicks on login button
    if not headlessOn:
        login_button.click()
    else:
        browser.execute_script("arguments[0].click();", login_button)
    
    time.sleep(0.25)
    
    try:
        # Check for login errors
        error_message = browser.find_element('class name','error')
        if error_message:
            print("Login failed. Please check your email and password.")
            return
    except:
        pass

    print("Login successful!")

    return

#######################################################################

# Browser user data [YOU MAY WANT TO CHANGE THIS]
browserData = 'C:\\Users\\toola\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default'
# Path to Browser of choice [YOU MAY WANT TO CHANGE THIS]
browserPath = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
# Email address
accEmail = 'YOUR EMAIL HERE'
# Password
accPassword = 'YOUR PASSWORD HERE'
# Use Browser without GUI
headlessOn = False

#######################################################################

# Make a GET request to the website
response = requests.get('https://levvvel.com/warframe-promo-codes/')

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

print("Finding codes. . .")
# Find all <a> elements with the class "aff-button"
a_elements = soup.find_all('a', {'class': 'aff-button'})
print("Found all codes.")

urls = []

print("Adding codes to list. . .")
# Loop through the list of elements and adds the href attribute of each element into a list urls
for a_element in a_elements:
    url = a_element.get('href')
    urls.append(url)
print("Finished adding codes to list.")

browser = option_configure(browserData, browserPath, headlessOn)

print("Attempting to log in. . .")
# logs into the website
login(accEmail, accPassword)

codeSize = len(urls)
currNum = 1

# for url in urls:
#     print(url)

# loop through all the promo codes and claim
for url in urls:
    # opens webpage where you can claim the promo code
    browser.get(url)

    # clicks the button to claim the promo code
    browser.find_element(
        By.XPATH, '//*[@id="promoCode"]/input[2]').click()
    
    time.sleep(1)

    # try:
    #     failure = browser.find_elements(By.XPATH, '/html/body/div[1]/div[3]/ul/li')
    #     if failure:
    #         print('ERROR:   Code not claimed (either already claimed or invalid)')
    #     else:
    #         print('SUCCESS: Code successfully claimed')
    # except:
    #     print('ERROR:   Unknown exception')

    try:
     # wait for the success message to appear on the page
        failure = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/ul/li[1]')))
        if failure:
            print("ERROR:   Code not claimed (either already claimed or invalid)")
    except:
        print('SUCCESS: Code successfully claimed')

    print(currNum, '/', codeSize)
    if currNum == 25:
        break
    currNum += 1

# Wait for the user to press Enter before closing the browser
input('Press Enter to close the browser...')
browser.quit()

# check if the webdriver process has terminated
webdriver_process = browser.service.process
if psutil.pid_exists(webdriver_process.pid):
    print('WebDriver process is still running.')
else:
    print('WebDriver process has terminated.')