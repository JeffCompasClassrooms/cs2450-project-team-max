from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import flask

app = flask.Flask(__name__)
# Specify the patath to ChromeDriver
chrome_driver_path = "/opt/homebrew/bin/chromedriver" #you'll need to put the path to YOUR chromedriver here
driver = webdriver.Chrome()
driver.executable_path=chrome_driver_path

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)
    print("--= BRYCE =--")
    print("--= Beginning Tests =--")
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']")))
    #1 login
    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")
    #2 Username field exists
    Username = driver.find_element(By.NAME, "username")
    if Username:
         print("[PASSED] - Username input Exists.")
    else:
        print("[FAILED] -  Username not found.")
    #3 password field exists
    password = driver.find_element(By.NAME, "password")
    if password :
         print("[PASSED] - Password input Exists.")
    else:
        print("[FAILED] -  Password not found.")
    #4 username takes input
    Username.send_keys("hi")
    if Username.get_attribute("value"):
        print("[PASSED] - Username getting input.")
    else:
        print("[FAILED] -  Username not getting input.")
    #5 password takes input
    password.send_keys("hi")
    if password.get_attribute("value"):
        print("[PASSED] - Password getting input.")
    else:
        print("[FAILED] -  Password not getting input.")
    #6 sign up button exists
    signUp =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']")))
    if signUp:
        print("[PASSED] - Sign Up Button Exists.")
    else:
        print("[FAILED] - Sign Up button not found.")
    #7 account created
    signUp.click()
    flash_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert"))
    )
    if flash_message:
        print("[PASSED] - Sign Up Complete.")
    else:
        print("[FAILED] - Sign Up not Complete.")
    #8 filled username for log in
    Username =WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "username"))
    )
    Username.send_keys("hi")
    if Username.get_attribute("value") == "hi":
        print("[PASSED] -Username entered")
    else:
        print("[FAILED] - Username not entered.")
    #9 filled password for log in
    Password = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "password"))
    )

    Password.send_keys("hi")

    if Password.get_attribute("value") == "hi":
        print("[PASSED] -Password entered")
    else:
        print("[FAILED] - Password not entered.")
    old_url=driver.current_url
    
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']")))
    login_button.click()
    #10 login 
    temp = WebDriverWait(driver, 10).until(EC.url_changes(old_url))
    
    if not temp == driver.current_url:
        print("[PASSED] -LOGGED IN")
    else:
        print("[FAILED] - Not logged in")
    

    

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()



# This is just a test commit to trigger GitHub Actions

