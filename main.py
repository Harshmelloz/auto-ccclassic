from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# NOTE: Paste the path to your chromedriver.exe here:
chrome_driver_path = "C:/Users/Harshmelloz/Documents/Chromedriver/chromedriver.exe"
# TODO: Get this automatically.

s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

# Get cookie clicker classic & its elements
driver.get(url='https://orteil.dashnet.org/experiments/cookie/')
cookie = driver.find_element(By.ID, "cookie")

start_time = time.time()
end_time = time.time() + 60 * 5
while time.time() < end_time:
    cookie.click()

print("5 minutess elapsed.")