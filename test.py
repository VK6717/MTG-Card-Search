from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = "C:\\Users\\Vlada\\Documents\\Python\\mtg_search_script\\msedgedriver.exe"  # změň na svoji cestu
#service = EdgeService(executable_path=driver_path)
driver = webdriver.Edge(executable_path="C:\\Users\\Vlada\\Documents\\Python\\mtg_search_script\\msedgedriver.exe")  # uprav cestu k sobě

# Wait for rows with class 'kusovky' to be present
# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "kusovkytext")))

# Find all rows in the table
rows = driver.find_elements(By.CLASS_NAME, "kusovkytext")

# Loop through rows in groups of 3 (product spans 3 rows)
for i in range(0, len(rows), 3):
    try:
        # Extract product name (row 1, td 2)
        product_name = rows[i].find_elements(By.TAG_NAME, "td")[1].text.strip()

        # Extract stock (row 3, td 2)
        stock = rows[i + 2].find_elements(By.TAG_NAME, "td")[1].text.strip()

        # Extract price (row 3, td 3)
        price = rows[i + 2].find_elements(By.TAG_NAME, "td")[2].text.strip()

        print(f"Product: {product_name}, Stock: {stock}, Price: {price}")
    except IndexError:
        print("❌ Error: Missing data for some rows")
