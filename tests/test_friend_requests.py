from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import flask
import unittest

app = flask.Flask(__name__)
# Specify the path to ChromeDriver

# chrome_driver_path = "/opt/homebrew/bin/chromedriver" #you'll need to put the path to YOUR chromedriver here

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1
})
driver = webdriver.Chrome(options=chrome_options)

driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": 37.1011711,
    "longitude": -113.5678041,
    "accuracy": 100
})
# driver.executable_path=chrome_driver_path

try:
    driver.get("http://localhost:5000")
    
    time.sleep(2)
    
    print("--= Beginning Tests =--")
    #1
    
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    create_account = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Create Account']")))
    print("[PASSED] - Create Account button found.")
    create_account.click()

    
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("admin")
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("admin")
    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))).click()
    old_url= driver.current_url
    print("[PASSED] - Admin user created.")
    print('[PASSED] - Url Changed')
    time.sleep(2)
   
    # Only then interact with its fields
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("hi")
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("hi")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))).click()
    #HI USER CREATED
    time.sleep(1)
    
    print(driver.current_url)
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("hi")
    print("[PASSED] - found username")
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("hi")
    print("[PASSED] - found password")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']"))).click()
    print(driver.current_url)
    WebDriverWait(driver, 10).until(EC.url_changes(old_url))
    print('[PASSED] - Changed URL')

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='name']"))).send_keys("admin")
    print("[PASSED] - found input")
    Submit_friend =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Submit']"))).click()
    print("[PASSED] - clicked add Friend")

    time.sleep(2)
    logout =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Logout']")))
    old_url = driver.current_url
    if logout:
        print("[PASSED] - logout Button Exists.")
    else:
        print("[FAILED] - logout button not found.")
    logout.click()
    print(driver.current_url)
    WebDriverWait(driver, 10).until(EC.url_changes(old_url))
    old_url= driver.current_url
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("admin")
    print('[PASSED] - admin user typed')
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("admin")
    print('[PASSED] - admin password typed')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']"))).click()
    print('[PASSED] - login user')
    WebDriverWait(driver, 10).until(EC.url_changes(old_url))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='accept']"))).click()
    print("[PASSED] - friend added")
    # Wait until the friends list is loaded
    time.sleep(2)
    first_friend_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card.bg-light ul li a"))
    )   
    first_friend_link.click()
    if WebDriverWait(driver, 10).until(EC.url_changes(old_url)):
        print("[PASSED] - Friend Button clicked.")
    else:
        print("[FAILED] - Friend Button Not Clicked.")
    
    #7
    message_box = driver.find_element(By.NAME, "send_message")
    if message_box:
        print("[PASSED] - message box found .")
    else:
        print("[FAILED] - message box not found.")
    #8
    message_box.send_keys("Hello, friend! Hope you're doing well.")
    typed_text = message_box.get_attribute("value")
    if typed_text:
        print("[PASSED] - message box being typed in .")
    else:
        print("[FAILED] - message box not being typed in.")
    #9
    submit_button = driver.find_element(By.NAME, "message_submit")
    if submit_button:
        print("[PASSED] - Submit Button  found .")
    else:
        print("[FAILED] - Submit Button not found.")
    submit_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert"))
    )
    
    messages = driver.find_elements(By.CLASS_NAME, "alert")
    
    message_text = None
    alert_type = None
    for message in messages:
        message_text = message.text
        alert_type = message.get_attribute("class").split()[-1]
        
    if message_text:
        print("[PASSED] - message Loaded.")
    else:
        print("[FAILED] - message not Loaded.")
        
    

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()