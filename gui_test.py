# NEEDED FOR LOGIN/CLAIM CODES
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from browser_option import option_configure
import time

# NEEDED FOR GUI
import customtkinter
from tkinter import filedialog
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    if isinstance(fontpath, str):
        pathbuf = create_string_buffer(fontpath.encode())
        AddFontResourceExW = windll.gdi32.AddFontResourceExW
    elif isinstance(fontpath, bytes):
        pathbuf = create_unicode_buffer(fontpath.decode())
        AddFontResourceExW = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or bytes')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceExW(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

loadfont("WarframeFanFont_b1.ttf")

# ------------------------------------------------------------------------------------------

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("custom.json")

root = customtkinter.CTk()
root.title('Warframe Code Claimer v0.6')
root.geometry("500x350")

# =================================================================

browserPath = ''
browserData = ''
accEmail = ''
accPassword = ''
# create a BooleanVar object
headlessOn = customtkinter.BooleanVar()
headlessOn.set(False)

# =================================================================

def login():
    global accEmail
    global accPassword
    global browser

    if(browserPath == '' or browserData == ''):
        print("Select your browser's exe path and/or default user profile directory")
        return
    accEmail = emailField.get()
    accPassword = passwordField.get()

    browser = option_configure(browserData, browserPath, headlessOn)
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
            print('Error while logging out to attempt relog-in')
    
    # enters email address
    email = browser.find_element(By.XPATH, '//*[@id="email-login"]/input')
    email.send_keys(accEmail)

    # enters password
    password = browser.find_element(By.XPATH, '//*[@id="password-login"]/input')
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

    findCodes()
    loginButton.configure(text="CLAIM", command=claim)

def findCodes():
    global urls
    
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

def claim():
    codeSize = len(urls)
    currNum = 1

    
    # loop through all the promo codes and claim
    for url in urls:
        # opens webpage where you can claim the promo code
        browser.get(url)

        # clicks the button to claim the promo code
        browser.find_element(
            By.XPATH, '//*[@id="promoCode"]/input[2]').click()
        
        time.sleep(1)

        try:
            failure = browser.find_elements(By.XPATH, '/html/body/div[1]/div[3]/ul/li')
            if failure:
                print('ERROR:   Code not claimed (either already claimed or invalid)')
            else:
                print('SUCCESS: Code successfully claimed')
        except:
            print('ERROR:   Unknown exception')

        print(currNum, '/', codeSize)
        if currNum == 10:
            break
        currNum += 1

def browse_browser():
    global browserPath
    browserPath = filedialog.askopenfilename(initialdir='', title='Select your Browser Directory', 
                                             filetypes=(('exe files', '*.exe'),('all files', '*.*')))
    path1.configure(text=browserPath[:25] + "...")

def browse_data():
    global browserData
    browserData = filedialog.askdirectory(initialdir='', title='Select your Default User Data')
    path2.configure(text=browserData[:25] + "...")

def toggle_checkbox():
    global headlessOn
    headlessOn = not headlessOn


###########################################################################################################


# main frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# title label
label = customtkinter.CTkLabel(master=frame, text="WARFRAnE\nCODE CLAIMER", font=("Warframe Fan Font", 20))
label.pack(pady=10)

# email field
emailField = customtkinter.CTkEntry(master=frame, placeholder_text = "Email Address")
emailField.pack(pady=5)

# password field
passwordField = customtkinter.CTkEntry(master=frame, placeholder_text = "Password", show="*")
passwordField.pack(pady=5)

# login button
loginButton = customtkinter.CTkButton(master=frame, text="LOG IN", command=login, font=("Warframe Fan Font", 11))
loginButton.pack(pady=10)

# check box to show browser
checkbox = customtkinter.CTkCheckBox(master=frame, text='Headless Browser', command=toggle_checkbox,
                                     variable=headlessOn, onvalue=True, offvalue=False, state=customtkinter.DISABLED)
checkbox.pack()

# Create a new frame for the buttons and center it
buttonFrame = customtkinter.CTkFrame(master=frame)
buttonFrame.pack(pady=10)

# browse button for browser
browse_button1 = customtkinter.CTkButton(master=buttonFrame, text='BROWSER', command=browse_browser,  font=("Warframe Fan Font", 11))
browse_button1.grid(row=0, column=0, padx=10)
# label to show directory to browser
path1 = customtkinter.CTkLabel(master=buttonFrame, text='No Directory Selected', corner_radius=1)
path1.grid(row=1, column=0, sticky="W", padx=10)

# browse button for browser user profile
browse_button2 = customtkinter.CTkButton(master=buttonFrame, text='PROFILE', command=browse_data, font=("Warframe Fan Font", 11))
browse_button2.grid(row=0, column=1, padx=10)
# label to show directory to browser profile
path2 = customtkinter.CTkLabel(master=buttonFrame, text='No Directory Selected', corner_radius=1)
path2.grid(row=1, column=1, sticky="W", padx=10)

root.mainloop()