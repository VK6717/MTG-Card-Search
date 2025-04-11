import re
import os
import csv
import time
import configparser
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# === Config ===
# Input Directory
BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "cards.csv"
# Output Directory
config_path = BASE_DIR / "config.ini"
config = configparser.ConfigParser()
if config_path.exists():
    config.read(config_path)
    output_path = config["DEFAULT"].get("output_dir", BASE_DIR / "out")
else:
    output_path = BASE_DIR / "out"
OUT_DIR = Path(output_path)
OUT_DIR.mkdir(parents=True, exist_ok=True)
# Output Files
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
OUTPUT_FILE = OUT_DIR / f"results_{timestamp}.csv"
OUTPUT_FILE_best = OUT_DIR / f"results_best_value_pick_{timestamp}.csv"
# Driver path
driver_path = BASE_DIR / "driver/msedgedriver.exe"  # Place driver in the same directory or update path

# === Initialize Driver ===
driver = webdriver.Edge(executable_path=str(driver_path))

# === Helper Functions ===
def find_number_of_pages():
    try:
        search_response = driver.find_element_by_xpath("//span[@class='kusovkytext']")
        links = search_response.find_elements_by_xpath("./a")
        match_total = re.search(r"Nalezeno\\s+(\\d+)\\s+kusov", search_response.text)
        total = int(match_total.group(1)) if match_total else None
        trailing_numbers = list(map(int, re.findall(r"\\b\\d+\\b", search_response.text)))
        max_page = max(trailing_numbers[1:]) if trailing_numbers else 1
        print(f"Nalezeno karet: {total}")
        print(f"Celkem stranek: {max_page}")
    except:
        links = []
        max_page = 1
        print("Nalezeno karet: Neznamo")
        print("Celkem stranek: 1")
    return max_page, links

def find_cards_on_page(card_name):
    tables = driver.find_elements_by_xpath("//table[@class='kusovkytext']")
    print(f"Nalezeno tabulek: {len(tables)}")
    table = tables[-1] if len(tables) > 1 else tables[0]
    rows = table.find_elements_by_tag_name('tr')
    cards = [rows[i:i+3] for i in range(0, len(rows), 3)]
    print(f"Nalezeno karet na strance: {len(cards)}")

    results = []
    for card in cards:
        try:
            name = card[0].find_element_by_xpath('./td[2]').text.strip()
            stock = card[2].find_element_by_xpath('./td[2]').text.strip()
            price = card[2].find_element_by_xpath('./td[3]').text.strip()
            url = f"https://www.cernyrytir.cz/index.php3?akce=3&limit=0&jmenokarty={card_name.replace(' ', '%20')}&edice_magic=libovolna&poczob=0&foil=A&triditpodle=ceny&hledej_pouze_magic=1&submit=Vyhledej"
            results.append({
                "search_name": card_name,
                "card_name": name,
                "stock_amount": stock,
                "price": price,
                "search_url": url
            })
        except Exception as e:
            print(f"Skipping card due to error: {e}")
    return results

# === Load Cards ===
with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
    card_list = [line.strip() for line in csvfile if line.strip()]
print(f"Cards to search: {card_list}")

# === Search and Collect Data ===
driver.get("https://www.cernyrytir.cz/index.php3?akce=3&sekce=prodejkusovkymagic")
all_cards = []

for card in card_list:
    print(f"Searching for: {card}")
    box = driver.find_element_by_name("jmenokarty")
    box.clear()
    box.send_keys(card)
    box.send_keys(Keys.ENTER)
    time.sleep(0.5)

    max_page, links = find_number_of_pages()
    for i in range(max_page):
        all_cards.extend(find_cards_on_page(card))
        if i < max_page - 1:
            links[i].click()
            time.sleep(0.3)

# === Write All Results ===
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["search_name", "card_name", "stock_amount", "price", "search_url"], delimiter=";")
    writer.writeheader()
    writer.writerows(all_cards)

# === Filter Best Value Cards ===
best_cards = {}
for card in all_cards:
    name = card["search_name"]
    try:
        stock = int(re.search(r'\d+', card["stock_amount"]).group())
        price = int(card["price"].replace("Kč", "").replace(" ", "").strip())
        if stock > 0:
            if name not in best_cards or price < int(best_cards[name]["price"].replace("Kč", "").replace(" ", "")):
                best_cards[name] = card
    except:
        continue

with open(OUTPUT_FILE_best, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["search_name", "card_name", "stock_amount", "price", "search_url"], delimiter=";")
    writer.writeheader()
    writer.writerows(best_cards.values())

# === Done ===
driver.quit()
print("✅ Search completed. Results saved.")
