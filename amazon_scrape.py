
import time
import requests
from bs4 import BeautifulSoup
import csv
import random

base_url = "https://www.amazon.in/s?k=bags"
back_url = "&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
page_suffix = "&page="
pages_to_scrape = 20

data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.203 ',
    'accept-language': 'en-US,en;q=0.9',
}

def get_product_info(product):
    product_url_element = product.find("a", class_="a-link-normal")
    if product_url_element:
        product_url = "https://www.amazon.in" + product_url_element["href"]
    else:
        product_url = "N/A"

    product_name_element = product.find("span", class_="a-text-normal")
    if product_name_element:
        product_name = product_name_element.get_text()
    else:
        product_name = "N/A"

    product_price_element = product.find("span", class_="a-price-whole")
    if product_price_element:
        product_price = product_price_element.get_text()
    else:
        product_price = "N/A"

    rating_element = product.find("span", class_="a-icon-alt")
    if rating_element:
        rating = rating_element.get_text().split()[0]
    else:
        rating = "N/A" 
    num_reviews_element = product.find("span", class_="a-size-base s-underline-text")
    if num_reviews_element:
        num_reviews = num_reviews_element.get_text()
    else:
        num_reviews = "0"

    return [product_url, product_name, product_price, rating, num_reviews]

max_retries = 5


for page in range(1, pages_to_scrape + 1):
    retries = 0
    while retries < max_retries:
        url = f"{base_url}{page_suffix}{page}{back_url}{str(page)}"
        # print(url)
        
        response = None
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 503:
                print("503 Error: Server overloaded. Retrying after delay...")
                retries += 1
                continue
            else:
                print(f"HTTP Error: {e}")
                break
        
        if response:
            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
            
            for product in products:
                data.append(get_product_info(product))
            
            time.sleep(2)
            break 
        
    time.sleep(2)



csv_filename = "amazon_pro.csv"
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])
    writer.writerows(data)

print("Scraping and writing to CSV complete.")