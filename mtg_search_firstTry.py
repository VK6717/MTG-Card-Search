
import csv
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

INPUT_FILE = "cards.csv"
OUTPUT_FILE = "results.csv"

# Load card names from CSV (1 card per line)
card_list = []
with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
    for row in csvfile:
        card = row.strip()
        if card:
            card_list.append(card)
print(card_list)

# Initialize Edge WebDriver
driver_path = "C:\\Users\\Vlada\\Documents\\Python\\mtg_search_script\\msedgedriver.exe"  # změň na svoji cestu
driver = webdriver.Edge(executable_path="C:\\Users\\Vlada\\Documents\\Python\\mtg_search_script\\msedgedriver.exe")  # uprav cestu k sobě

# Open website
driver.get("https://www.cernyrytir.cz")
time.sleep(3)

# Prepare list to collect output rows
output_rows = []

for card in card_list:
    print(f"Searching for: {card}")
    search_box = driver.find_element(By.NAME, "vyhledejkomplet")
    search_box.clear()
    search_box.send_keys(card)
    search_box.send_keys(Keys.RETURN)

    time.sleep(0.5)  # wait for page to load

    # Find all tables with the 'kusovkytext' class
    tables = driver.find_elements(By.CLASS_NAME, "kusovkytext")
    print(tables.__len__())

    # Loop through each table (product)
    for table in tables:
        # Make sure there are enough rows (3 rows per product)
        rows = table.find_elements(By.TAG_NAME, "tr")
        if len(rows) >= 3:
            # Extract product name (row 1, td 2)
            product_name = rows[0].find_elements(By.TAG_NAME, "td")[1].text.strip()

            # Extract stock (row 3, td 2)
            stock = rows[2].find_elements(By.TAG_NAME, "td")[1].text.strip()

            # Extract price (row 3, td 3)
            price = rows[2].find_elements(By.TAG_NAME, "td")[2].text.strip()

            print(f"Product: {product_name}, Stock: {stock}, Price: {price}")
        else:
            print("Skipping product due to missing rows")