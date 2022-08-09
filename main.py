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

item_top_limit = 10
items_bought = {}


def buy_from_store():
    # Get upgrade item ids, item prices.
    items = driver.find_elements(By.CSS_SELECTOR, "#store div")
    item_ids = [item.get_attribute("id") for item in items if item.get_attribute("id") != '']

    all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
    item_prices = [price.text for price in all_prices if price.text != '']
    for i in range(len(item_prices)):
        if item_prices[i] != '':
            item_prices[i] = int(item_prices[i].split("-")[1].lstrip(" ").replace(",", ""))

    # Make upgrades dict from ids and prices
    cookie_upgrades = {}
    for i in range(len(item_prices)):
        cookie_upgrades[item_prices[i]] = item_ids[i]
    # pprint(cookie_upgrades)

    # If first run, fill out the keys with the item names
    if items_bought == {}:
        for item_id in item_ids:
            items_bought[item_id] = 0

    # Get current cookie count
    cur_cookies = int(driver.find_element(By.ID, "money").text.replace(",", ""))

    # Find the highest value item to buy
    max_price = 0
    min_price = min(item_prices)
    for key in cookie_upgrades.keys():
        if cur_cookies >= key:
            max_price = key

    # Find element and click to buy it
    item_to_buy = driver.find_element(By.ID, cookie_upgrades[max_price])
    id_to_buy = item_to_buy.get_attribute("id")
    if items_bought[id_to_buy] < item_top_limit:
        item_to_buy.click()
        items_bought[id_to_buy] += 1
        print(f"[{cur_cookies}] Bought {cookie_upgrades[max_price][3:]} for {max_price}")
    else:
        instead = driver.find_element(By.ID, cookie_upgrades[min_price])
        instead_id = instead.get_attribute("id")
        items_bought[instead_id] += 1
        instead.click()
        print(f"[{cur_cookies}] Max buy is {cookie_upgrades[max_price][3:]} but we already have {items_bought[id_to_buy]}. "
              f"Bought cheapest item {cookie_upgrades[min_price][3:]} instead.")


duration = input("Type number of hours to run or press ENTER to run for 5 minutes: ")
if duration == "":
    timeout = time.time() + 60 * 5
else:
    try:
        timeout = time.time() + 60 * 60 * float(duration)
    except TypeError:
        timeout = time.time() + 60 * 60 * 24
        print("That's not a valid number. Running for 24 hours.")


next5sec = time.time() + 5
count = 0
while time.time() < timeout:
    cookie.click()
    if time.time() >= next5sec:
        buy_from_store()
        next5sec = time.time() + 5
    count += 1
print(f"Timeout reached, program stopped after {count} loops.")

# Get final cookies per second
cps = driver.find_element(By.ID, "cps").text
print(f"Final {cps}")