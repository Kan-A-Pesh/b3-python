import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import re

PRODUCT_URL = "https://books.toscrape.com/catalogue/mesaerion-the-best-science-fiction-stories-1800-1849_983/index.html"


def get_product_info(url):
    print("Extracting:", url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_info = {}

    # Fetch the product information
    product_info["product_page_url"] = url

    product_info["universal_product_code"] = (
        soup.find("th", string="UPC").find_next_sibling("td").string
    )

    product_info["title"] = soup.find("h1").string

    product_info["price_excluding_tax"] = (
        soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
    )

    product_info["price_including_tax"] = (
        soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
    )

    # Get availability as a number with regex (or N/A if not available)
    availability = soup.find("th", string="Availability").find_next_sibling("td").string
    availability = re.search(r"\d+", availability).group()
    product_info["number_available"] = availability if availability else "N/A"

    desc = soup.find("div", id="product_description")
    if desc:
        product_info["product_description"] = desc.find_next_sibling("p").string
    else:
        product_info["product_description"] = "N/A"

    product_info["category"] = (
        soup.find("ul", class_="breadcrumb").find_all("a")[2].string
    )

    # Get rating from 2nd class of "p.star-rating" tag
    rating_tag = soup.find("p", class_="star-rating")
    if rating_tag:
        ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        product_info["review_rating"] = ratings[rating_tag["class"][1]]
    else:
        product_info["review_rating"] = "N/A"

    # Get absolute url from relative
    image_relative_url = soup.find("div", id="product_gallery").find("img")["src"]
    product_info["image_url"] = urljoin(url, image_relative_url)

    return product_info


def save_to_csv(data, filename="product_data.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    product_data = get_product_info(PRODUCT_URL)
    save_to_csv([product_data])
    print("Data extracted and saved to product_data.csv")
