import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
from phase1 import get_product_info, save_to_csv

# Test one page
# CATEGORY_URL = (
#     "https://books.toscrape.com/catalogue/category/books/classics_6/index.html"
# )

# Test with pagination
CATEGORY_URL = (
    "https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html"
)


def get_category_products_data(category_url):
    products_urls = get_category_products_urls(category_url)

    product_data = []
    for url in products_urls:
        product_data.append(get_product_info(url))

    return product_data


def get_products_urls_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    products_urls = []
    for product in soup.find_all("article", class_="product_pod"):
        products_urls.append(urljoin(page_url, product.h3.a["href"]))

    return products_urls, soup


def get_category_products_urls(page_url, previous_urls=[]):
    products_urls, soup = get_products_urls_from_page(page_url)
    products_urls.extend(previous_urls)

    if soup.find("li", class_="next"):
        return get_category_products_urls(
            urljoin(page_url, soup.find("li", class_="next").a["href"]),
            products_urls,
        )
    else:
        return products_urls


if __name__ == "__main__":
    product_data = get_category_products_data(CATEGORY_URL)
    save_to_csv(product_data)
    print("Data extracted and saved to product_data.csv")
