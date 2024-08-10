import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

URL = "https://www.homedepot.com"

response = requests.get(URL, headers=headers)
print(f"Status Code: {response.status_code}")

soup = BeautifulSoup(response.content, "html.parser")

# Find the price element
price_element = soup.find("div", {"data-testid": "price-format__main-price"})
if price_element:
    price = price_element.text.strip()
    print(f"Price: {price}")
else:
    print("Price not found")

# Find the product title
title_element = soup.find("h1", {"class": "product-details__title"})
if title_element:
    title = title_element.text.strip()
    print(f"Title: {title}")
else:
    print("Title not found")

# Find the model number
model_element = soup.find("h2", {"class": "product-info-bar__model"})
if model_element:
    model = model_element.text.strip()
    print(f"Model: {model}")
else:
    print("Model not found")