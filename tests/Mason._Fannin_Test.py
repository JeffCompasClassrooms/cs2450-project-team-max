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

    # Step 2: Perform login
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")

        username_input.send_keys("test_user")  # Replace with a valid username
        password_input.send_keys("test_password")  # Replace with a valid password
        login_button.click()
        print("Current URL after login:", driver.current_url)
        # Wait for the page to load after login
        WebDriverWait(driver, 10).until(
            EC.url_contains("http://localhost:5000/")  # Replace with the URL the user is redirected to after login
        )
        print("[PASSED] - Login successful.")
    except Exception as e:
        print("[FAILED] - Login failed:", e)
        raise
        
    # Step 3: Navigate to the settings page
    driver.get("http://localhost:5000/settings")
    print("--= Navigated to Settings Page =--")

    # Test 2: Verify the settings page loads
    try:
        settings_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        if settings_header.text.strip() == "Settings":
            print("[PASSED] - Settings page loaded successfully.")
        else:
            print("[FAILED] - Settings page header is incorrect.")
    except Exception as e:
        print("[FAILED] - Settings page did not load:", e)
    
    # Test 3: Verify the username input field exists
    try:
        username_input = driver.find_element(By.NAME, "username")
        print("[PASSED] - Username input field exists.")
    except Exception as e:
        print("[FAILED] - Username input field not found:", e)

    # Test 4: Verify the update username button exists
    try:
        update_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Update Info']")
        print("[PASSED] - Update username button exists.")
    except Exception as e:
        print("[FAILED] - Update username button not found:", e)

    # Test 5: Update the username
    try:
        username_input = driver.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys("new_username")
        update_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Update Info']")
        update_button.click()

        # Wait for the success message to appear
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ""))
        )
        if "Username updated successfully" in success_message.text.strip():  # Replace with the actual success message
            print("[PASSED] - Username updated successfully.")
        else:
            print("[FAILED] - Username update failed.")
    except Exception as e:
        print("[FAILED] - Error while updating username:", e)

    # Test 6: Verify the current password input field exists
    try:
        current_password_input = driver.find_element(By.NAME, "current_password")
        print("[PASSED] - Current password input field exists.")
    except Exception as e:
        print("[FAILED] - Current password input field not found:", e)

    # Test 7: Verify the new password input field exists
    try:
        new_password_input = driver.find_element(By.NAME, "new_password")
        print("[PASSED] - New password input field exists.")
    except Exception as e:
        print("[FAILED] - New password input field not found:", e)

    # Test 8: Change the password
    try:
        current_password_input = driver.find_element(By.NAME, "current_password")
        new_password_input = driver.find_element(By.NAME, "new_password")
        confirm_password_input = driver.find_element(By.NAME, "confirm_password")
        current_password_input.send_keys("old_password")
        new_password_input.send_keys("new_password")
        confirm_password_input.send_keys("new_password")
        change_password_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Change Password']")
        change_password_button.click()
        time.sleep(2)  # Wait for the page to reload
        success_message = driver.find_element(By.CLASS_NAME, "alert-success")
        if "Password changed successfully" in success_message.text:
            print("[PASSED] - Password changed successfully.")
        else:
            print("[FAILED] - Password change failed.")
    except Exception as e:
        print("[FAILED] - Error while changing password:", e)

    # Test 9: Verify the delete account button exists
    try:
        delete_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete Account']")
        print("[PASSED] - Delete account button exists.")
    except Exception as e:
        print("[FAILED] - Delete account button not found:", e)

    # Test 10: Delete the account
    try:
        delete_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete Account']")
        delete_account_button.click()
        time.sleep(2)  # Wait for the page to reload
        success_message = driver.find_element(By.CLASS_NAME, "alert-success")
        if "Your account has been deleted" in success_message.text:
            print("[PASSED] - Account deleted successfully.")
        else:
            print("[FAILED] - Account deletion failed.")
    except Exception as e:
        print("[FAILED] - Error while deleting account:", e)

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()