from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def option_configure(browserData, browserPath, headlessOn):
    # ignores certain error and adds browser user data and browser path
    option = webdriver.ChromeOptions()
    option.add_argument('--ignore-certificate-errors')
    option.add_argument("--disable-webgl")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    option.add_argument("user-data-dir=" + browserData)
    if(headlessOn):
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
    option.binary_location = browserPath

    # creates brower driver
    s = Service("/chromedriver")
    browser = webdriver.Chrome(service=s, options=option)
    # if(not headlessOn):
    #     browser.maximize_window()
    return browser