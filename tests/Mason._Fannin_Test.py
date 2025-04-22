from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the path to ChromeDriver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--user-data-dir=/tmp/selenium_user_data")
chrome_driver_path = "/usr/local/bin/chromedriver" #you'll need to put the path to YOUR chromedriver here
service = Service(chrome_driver_path)
driver = webdriver.Chrome(options=options)


try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests =--")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")

    # Step 2: Navigate to the Create Profile page
    driver.get("http://localhost:5000/profileScreen")
    print("--= Beginning Tests for Create Profile Page =--")

    # Test 2: Verify the Create Profile page loads
    try:
        profile_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "legend"))
        )
        if profile_header.text.strip() == "Create Profile":
            print("[PASSED] - Create Profile page loaded successfully.")
        else:
            print("[FAILED] - Create Profile page header is incorrect.")
    except Exception as e:
        print("[FAILED] - Create Profile page did not load:", e)

    # Test 3: Verify the Full Name input field exists and is required
    try:
        full_name_input = driver.find_element(By.NAME, "Fullname")
        if full_name_input.get_attribute("required"):
            print("[PASSED] - Full Name input field exists and is required.")
        else:
            print("[FAILED] - Full Name input field is not marked as required.")
    except Exception as e:
        print("[FAILED] - Full Name input field not found:", e)

    # Test 4: Verify the Age input field exists and is required
    try:
        age_input = driver.find_element(By.NAME, "age")
        if age_input.get_attribute("required"):
            print("[PASSED] - Age input field exists and is required.")
        else:
            print("[FAILED] - Age input field is not marked as required.")
    except Exception as e:
        print("[FAILED] - Age input field not found:", e)

    # Test 5: Verify the Instrument dropdown allows multiple selections
    try:
        instrument_dropdown = driver.find_element(By.ID, "instrument")
        if instrument_dropdown.get_attribute("multiple"):
            print("[PASSED] - Instrument dropdown allows multiple selections.")
        else:
            print("[FAILED] - Instrument dropdown does not allow multiple selections.")
    except Exception as e:
        print("[FAILED] - Instrument dropdown not found:", e)

    # Test 6: Verify the Genre dropdown contains all expected options
    try:
        genre_dropdown = driver.find_element(By.ID, "genre")
        options = [option.text for option in genre_dropdown.find_elements(By.TAG_NAME, "option")]
        expected_options = [
            "Rock", "Metal", "Jazz", "Blues", "Classical", "Indie", "Country",
            "Hip Hop", "Reggae", "Folk", "Punk", "Pop Punk", "Alternative", "Shoe Gaze"
        ]
        if all(option in options for option in expected_options):
            print("[PASSED] - Genre dropdown contains all expected options.")
        else:
            print("[FAILED] - Genre dropdown is missing some expected options.")
    except Exception as e:
        print("[FAILED] - Genre dropdown not found:", e)

    # Test 7: Verify the Covers dropdown functionality
    try:
        covers_dropdown = driver.find_element(By.ID, "covers")
        covers_dropdown.click()
        options = [option.text for option in covers_dropdown.find_elements(By.TAG_NAME, "option")]
        if "Create New Music" in options and "Perform Cover Songs" in options:
            print("[PASSED] - Covers dropdown contains expected options.")
        else:
            print("[FAILED] - Covers dropdown is missing expected options.")
    except Exception as e:
        print("[FAILED] - Covers dropdown not found:", e)

    # Test 8: Verify the Travel dropdown functionality
    try:
        travel_dropdown = driver.find_element(By.ID, "travel")
        travel_dropdown.click()
        options = [option.text for option in travel_dropdown.find_elements(By.TAG_NAME, "option")]
        if "Yes" in options and "No" in options:
            print("[PASSED] - Travel dropdown contains expected options.")
        else:
            print("[FAILED] - Travel dropdown is missing expected options.")
    except Exception as e:
        print("[FAILED] - Travel dropdown not found:", e)

    # Test 9: Verify the Profile Picture upload field exists
    try:
        profile_picture_upload = driver.find_element(By.ID, "mediaUpload")
        if profile_picture_upload.get_attribute("accept") == "image/*":
            print("[PASSED] - Profile Picture upload field exists and accepts images.")
        else:
            print("[FAILED] - Profile Picture upload field does not accept images.")
    except Exception as e:
        print("[FAILED] - Profile Picture upload field not found:", e)

    # Test 10: Verify the Save button is there
    try:
        save_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='save']"))
        )
        print("[PASSED] - Save button exists.")
    except Exception as e:
        print("[FAILED] - Save button not found:", e)
except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()