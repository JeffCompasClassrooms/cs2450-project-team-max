from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
os.system("pkill -f chrome")  # Kills any running Chrome processes

# Specify the path to ChromeDriver
chrome_driver_path = "/root/cs2450-project-team-max/chromedriver-linux64/chromedriver"
service = Service(chrome_driver_path)

# Add Chrome options
options = Options()
options.add_argument("--user-data-dir=/tmp/chrome-profile")  # Use a unique profile
options.add_argument("--no-sandbox")  # Helps with running Chrome in some environments
options.add_argument("--disable-dev-shm-usage")  # Prevents Chrome crash in Docker/Linux
options.add_argument("--headless")  # Run Chrome in headless mode

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests =--")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()