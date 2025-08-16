import requests
from bs4 import BeautifulSoup

# Create a Session object to persist cookies
session = requests.Session()

LOGIN_URL = "http://quotes.toscrape.com/login"
HOME_URL = "http://quotes.toscrape.com/"

print("Getting the login page to find the CSRF token...")

try:
    # Use the session to make a GET request to the login page
    response = session.get(LOGIN_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    print(f"Successfully found CSRF Token: {csrf_token}")

    # --- Submit the Login Form ---
    print("Attempting to log in...")
    login_data = {
        'username': 'admin',
        'password': 'admin',
        'csrf_token': csrf_token
    }
    response = session.post(LOGIN_URL, data=login_data)
    response.raise_for_status()

    # --- Verify Login ---
    print("Verifying login status...")
    response = session.get(HOME_URL)
    
    if "Logout" in response.text:
        print("Login successful! We are authenticated.")
        soup = BeautifulSoup(response.text, 'html.parser')
        author_links = [a['href'] for a in soup.select('a[href*="/author/"]')]
        print(f"Found {len(set(author_links))} unique author pages to scrape.")
    else:
        print("Login failed. 'Logout' link not found.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")