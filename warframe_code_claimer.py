import requests
from bs4 import BeautifulSoup

url = 'https://www.warframe.com/login'

# create a session object
session = requests.Session()

# get the login page to retrieve the CSRF token
login_page = session.get(url)
soup = BeautifulSoup(login_page.text, 'html.parser')
csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

print("CSRF Token: {}".format(csrf_token))

# define the login data with the retrieved CSRF token
login_data = {
    'email': 'ENTER YOUR EMAIL HERE',
    'password': 'ENTER YOUR PASSWORD HERE',
    '_token': csrf_token,
    'next': '/',
}

print('url before login: {}'.format(response.url))

# log in to the website
response = session.post(url, data=login_data, headers={'Referer': url})
print('url after login: {}'.format(response.url))
print('response:\n{}'.format(response))

print("Status Code: {}".format(response.status_code))
# check if login was successful
if response.url == 'https://www.warframe.com/':
    print("Login successful!")
else:
    print("Login failed.")

session.cookies.clear_session_cookies()

# check if session cookie is present in the response headers
if 'sessionid' in response.cookies:
    print("Logout unsuccessful, session cookie still present.")
else:
    print("Logout successful, session cookie has been deleted.")