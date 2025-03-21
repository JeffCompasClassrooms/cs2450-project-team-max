from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Specify the path to ChromeDriver
chrome_driver_path = "/Users/greta/chromedriver" #you'll need to put the path to YOUR chromedriver here
driver = webdriver.Chrome() #executable_path=chrome_driver_path

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Jesse Betts =--")

#test 1 Login Button
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")


#test 2 background color
    background_color = driver.find_element(By.CSS_SELECTOR, "body")
    if background_color.value_of_css_property("background-color") == "rgba(216, 210, 164, 1)":
        print("[PASSED] - Background color is beige.")
    else:
        print("[FAILED] - Background colr is not beige.")

#Test 3 sign up button
    signup_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Sign Up']")

    if signup_button:
        print("[PASSED] - Sign Up Button Exists.")
    else:
        print("[FAILED] - Sign Up button not found.")

#Test 4 purple box
    box_color = driver.find_element(By.CSS_SELECTOR, "div.card.card-body.bg-light") 
    if box_color.value_of_css_property("background-color") == "#4F5B84": 
        print("[PASSED] - Purple box color is Correct.")
    else:
        print("[FAILED] - Color is not purple.")



#Test 5 Title
    title_size = driver.find_element(By.CSS_SELECTOR, "h1")
    if title_size.value_of_css_property("font-size") == "30px":
        print("[PASSED] - Title text size is correct.")
    else:
        print("[FAILED] - Title text size is incorrect.")

#Test 6 Title name
    title_name = driver.find_element(By.CSS_SELECTOR, "a")
    if title_name.text == "Maxes Music Matcher":
        print("[PASSED] - Title text is correct.")
    else:
        print("[FAILED] - Title text is incorrect.")

#Test 7 Subtitle
    title_size = driver.find_element(By.CSS_SELECTOR, "p.lead")
    if title_size.value_of_css_property("font-size") == "18px":
        print("[PASSED] -  Subtitle text size is correct.")
    else:
        print("[FAILED] - Subtitle text size is incorrect.")

#Test 8 subtitle message
    title_size = driver.find_element(By.CSS_SELECTOR, "p.lead")
    if title_size.text == "Are YOU ready to rock!":
        print("[PASSED] - Subtitle text message is correct.")
    else:
        print("[FAILED] - Subtitle text message is incorrect.")    

#Test 9 purple bar
    box_color = driver.find_element(By.CSS_SELECTOR, "nav.navbar.navbar-expand-lg.navbar-dark.bg-primary")  
    if box_color.value_of_css_property("background-color") != "rgb(165, 42, 42)":  
        print("[PASSED] - Bar color is visable.")
    else:
        print("[FAILED] - Bar color is brown.")

        
#Test 10 nav bar
    navbar = driver.find_elements(By.CSS_SELECTOR, "nav.navbar.navbar-expand-lg.navbar-dark.bg-primary")  # Target the <nav> element
    if navbar:
        print("[PASSED] - Navbar exists.")
    else:
        print("[FAILED] - Navbar does not exist.")



except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()



