import requests
from bs4 import BeautifulSoup

# # URL to scrape
# url = 'your_product_page_url'
#
# # Send request to fetch page content
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# Open your HTML file
with open('full_html.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all product tables
tables = soup.find_all('table', class_='kusovkytext')
print(len(tables))

# Loop through each table and extract data
for table in tables:
    rows = table.find_all('tr')
    print(len(rows))
    num_products = len(rows) // 3
    print(f"Number of products found: {num_products}")
    for i in range(0, num_products, 1):
        product_name = rows[3*i].find_all('td')[1].text.strip()
        stock = rows[3*i+2].find_all('td')[1].text.strip()
        price = rows[3*i+2].find_all('td')[2].text.strip()
        print(f"Product: {product_name}, Stock: {stock}, Price: {price}")
