import requests
import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class TestLikeButton(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Get geolocation from ipinfo.io
        response = requests.get("https://ipinfo.io")
        location = response.json()
        loc = location['loc']
        cls.latitude, cls.longitude = map(float, loc.split(","))

        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1
        })

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": cls.latitude,
            "longitude": cls.longitude,
            "accuracy": 100
        })
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_full_flow(self):
        driver = self.driver
        wait = self.wait

        driver.get("http://localhost:5000")
        time.sleep(2)

        print("--= Beginning Tests =--")
        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Create Account']"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("test1")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("test1")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))).click()
        print("[PASSED] - test1 user created.")
        old_url = driver.current_url
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("test2")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("test2")
        print(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))).click()
        time.sleep(1)
        print("[PASSED] - test2 user created.")


        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("test1")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("test1")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']"))).click()
        WebDriverWait(driver, 10).until(EC.url_changes(old_url))
        print("[PASSED] - test1 logged in.")


        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='name']"))).send_keys("test2")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Submit']"))).click()
        print("[PASSED] - test1 send request to test2.")

        time.sleep(2)
        old_url = driver.current_url       
        navbar =driver.find_element(By.ID, "navbarColor01")
        navbar2 = driver.find_element(By.ID, "help-me")

       
        time.sleep(1)   
        print(navbar.is_enabled())
        is_visible = navbar.is_displayed()
        print(is_visible)
        navbar.click()
        print(navbar2.is_enabled())
        is_visible = navbar2.is_displayed()
        print(is_visible)
        
        print(old_url)
        time.sleep(1)   
        # logout =
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Logout']").click()
        # print('logout found')
        # print(logout.is_enabled())
        # print(logout.is_displayed())
        # print(logout.rect)
        # print(logout.get_attribute('value'))
        
         
       
       
        # logout.click()
       
        print("[PASSED] - test1 logged out.")

        print(driver.current_url)
        old_url = driver.current_url
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("test2")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("test2")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']"))).click()
        WebDriverWait(driver, 10).until(EC.url_changes(old_url))
        print("[PASSED] - test2 signed in.")


        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[type='submit'][value='accept']"))).click()
        time.sleep(2)
        print("[PASSED] - test2 accepted friend request.")
        print("--= All Tests Passed =--")

if __name__ == "__main__":
    unittest.main()
