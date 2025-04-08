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
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("admin")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("admin")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))).click()
        print("[PASSED] - Admin user created.")
        old_url = driver.current_url
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("hi")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("hi")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']"))).click()
        time.sleep(1)

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("hi")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("hi")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']"))).click()
        WebDriverWait(driver, 10).until(EC.url_changes(old_url))

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='name']"))).send_keys("admin")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Submit']"))).click()
        time.sleep(2)
        old_url = driver.current_url
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler"))).click()
        print('clicked')

        wait.until(driver.find_element((By.CSS_SELECTOR, "input[type='submit'][value='Logout']"))).click()
        WebDriverWait(driver, 10).until(EC.url_changes(old_url))

        old_url = driver.current_url
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("admin")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("admin")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Login']"))).click()
        WebDriverWait(driver, 10).until(EC.url_changes(old_url))

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[type='submit'][value='accept']"))).click()
        time.sleep(2)

        first_friend_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card.bg-light ul li a"))
        )
        first_friend_link.click()
        WebDriverWait(driver, 10).until(EC.url_changes(old_url))

        message_box = driver.find_element(By.NAME, "send_message")
        message_box.send_keys("Hello, friend! Hope you're doing well.")
        typed_text = message_box.get_attribute("value")
        self.assertTrue(typed_text)

        submit_button = driver.find_element(By.NAME, "message_submit")
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        messages = driver.find_elements(By.CLASS_NAME, "alert")
        self.assertTrue(any(msg.text for msg in messages))

        print("--= All Tests Passed =--")

if __name__ == "__main__":
    unittest.main()
