from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import flask

app = flask.Flask(__name__)
# Specify the path to ChromeDriver

# chrome_driver_path = "/opt/homebrew/bin/chromedriver" #you'll need to put the path to YOUR chromedriver here

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
# driver.executable_path=chrome_driver_path

try:
    print('in')
    driver.get("http://localhost:5000/loginscreen")
    driver.add_cookie({"name": "username", "value": "admin"})
    driver.add_cookie({"name": "password", "value": "admin"})
    time.sleep(2)
    
    print("--= Beginning Tests =--")
    #1
    if driver.get_cookie('username'):
        print("[PASSED] - username cookie set")
    else:
        print("[FAILED] - username cookie not found.")
    #2
    if driver.get_cookie('password'):
        print("[PASSED] - password cookie set")
    else:
        print("[FAILED] - password cookie not found.")
    #3

    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']")))
    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")
    old_url = driver.current_url
    
    
    #4
    login_button.click()
    
    if WebDriverWait(driver, 10).until(EC.url_changes(old_url)):
        print("[PASSED] - Login Button clicked.")
    else:
        print("[FAILED] - Login Button Not Clicked.")
    
    
    #5
    old_url = driver.current_url
    # Wait until the friends list is loaded
    first_friend_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card.bg-light ul li a"))
    )   
    first_friend_link.click()
    if WebDriverWait(driver, 10).until(EC.url_changes(old_url)):
        print("[PASSED] - Friend Button clicked.")
    else:
        print("[FAILED] - Friend Button Not Clicked.")
    
    
    #6
    message_text= None
    alert_type = None
    count = 0
    messages = driver.find_elements(By.CLASS_NAME, "alert")
    for index, message in enumerate(messages):
        message_text = message.text  
        alert_type = message.get_attribute("class").split()[-1]  
        count+=1
        
    if message_text:
        print("[PASSED] - message Loaded.")
    else:
        print("[FAILED] - message not Loaded.")
    
    
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