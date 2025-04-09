import re
import os
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def find_number_of_pages():
    try:
        search_response = driver.find_element_by_xpath("//span[@class='kusovkytext']")
        links = search_response.find_elements_by_xpath("./a")
        # Extract the total number
        match_total = re.search(r"Nalezeno\s+(\d+)\s+kusových", search_response.text)
        total = int(match_total.group(1)) if match_total else None
        trailing_numbers = re.findall(r"\b\d+\b", search_response.text)  # Find all trailing numbers
        trailing_numbers = list(map(int, trailing_numbers))  # Convert to integers
        max_page = max(trailing_numbers[
                       1::]) if trailing_numbers else None  # The highest number in sequence at the end (after the colon)
        print(f"Nalezeno karet: {total}")
        print(f"Celkem stránek: {max_page}")
    except:
        links = []
        max_page = 1
        print(f"Nalezeno karet: Neznámo")
        print(f"Celkem stránek: 1")
    return max_page, links


def find_cards_on_page(card_name):
    cards_table_list = driver.find_elements_by_xpath("//table[@class='kusovkytext']")
    print(f"Nalezeno tabulek: {len(cards_table_list)}")
    if len(cards_table_list) > 1:
        cards_table = cards_table_list[-1]
    else:
        cards_table = cards_table_list[0]

    rows = cards_table.find_elements_by_tag_name('tr')
    cards_found = [rows[i:i + 3] for i in range(0, len(rows), 3)]
    print(f"Nalezeno karet na stránce: {len(cards_found)}")

    search_names = []
    names = []
    stocks = []
    prices = []
    URLs = []

    for card in cards_found:
        search_name = card_name
        search_names.append(search_name)
        name = (card[0].find_element_by_xpath('./td[2]').text)
        names.append(name)
        stock = (card[2].find_element_by_xpath('./td[2]').text)
        stocks.append(stock)
        price = (card[2].find_element_by_xpath('./td[3]').text)
        prices.append(price)
        URL = f"https://www.cernyrytir.cz/index.php3?akce=3&limit=0&jmenokarty={card_name.replace(' ', '%20')}&edice_magic=libovolna&poczob=0&foil=A&triditpodle=ceny&hledej_pouze_magic=1&submit=Vyhledej"
        URLs.append(URL)

    return search_names, names, stocks, prices, URLs


# Main
INPUT_FILE = "cards.csv"
OUTPUT_FILE = f"out/results_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
OUTPUT_FILE_best = f"out/results_best_value_pick_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

# Create output folder if it doesn't exist
os.makedirs("out", exist_ok=True)

all_search_names = []
all_names = []
all_stocks = []
all_prices = []
all_URLs = []

driver_path = "C:\\Users\\Vlada\\Documents\\Python\\mtg_search_script\\msedgedriver.exe"  # změň na svoji cestu
driver = webdriver.Edge(
    executable_path="C:\\Users\\Vlada\\Documents\\Python\\mtg_search_script\\msedgedriver.exe")  # uprav cestu k sobě

# Open website
website = "https://www.cernyrytir.cz/index.php3?akce=3&sekce=prodejkusovkymagic"
driver.get(website)

# Load card names from CSV (1 card per line)
card_list = []
with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
    for row in csvfile:
        card = row.strip()
        if card:
            card_list.append(card)
print(card_list)

# Search all the cards in the list
for card in card_list:
    print(f"Searching for: {card}")

    search_box = driver.find_element_by_name("jmenokarty")
    search_box.clear()
    search_box.send_keys(card)
    search_box.send_keys(Keys.ENTER)
    time.sleep(0.5)  # wait for page to load

    max_page, links = find_number_of_pages()
    for i in range(0, max_page, 1):
        max_page, links = find_number_of_pages()
        search_name, name, stock, price, URL = find_cards_on_page(card)
        all_search_names.append(search_name)
        all_names.append(name)
        all_stocks.append(stock)
        all_prices.append(price)
        all_URLs.append(URL)
        if i < max_page - 1:
            links[i].click()

# flatten nested list
all_search_names = [item for sublist in all_search_names for item in sublist]
all_names = [item for sublist in all_names for item in sublist]
all_stocks = [item for sublist in all_stocks for item in sublist]
all_prices = [item for sublist in all_prices for item in sublist]
all_URLs = [item for sublist in all_URLs for item in sublist]

# Prepare output format
output_rows = []
for i, name in enumerate(all_names):
    print(f"Product číslo {i + 1}: {all_names[i]}, Stock: {all_stocks[i]}, Price: {all_prices[i]}, URL: {all_URLs[i]}")
    output_rows.append({
        "search_name": all_search_names[i],
        "card_name": all_names[i],
        "stock_amount": all_stocks[i],
        "price": all_prices[i],
        "search_url": all_URLs[i]
    })

# Find best value cards
best_value_cards = {}
for card in output_rows:
    name = card["search_name"]
    if int(re.search(r'\d+', card["stock_amount"]).group()) > 0:
        if name not in best_value_cards or int(card["price"].replace(" Kč", "").strip()) < \
                int(best_value_cards[name]["price"].replace(" Kč", "").strip()):
            best_value_cards[name] = card

# Write all results
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["search_name", "card_name", "stock_amount", "price", "search_url"],
                            delimiter=";")
    writer.writeheader()
    writer.writerows(output_rows)

# Write best value for each card
with open(OUTPUT_FILE_best, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["search_name", "card_name", "stock_amount", "price", "search_url"],
                            delimiter=";")
    writer.writeheader()
    writer.writerows(best_value_cards.values())

driver.quit()
