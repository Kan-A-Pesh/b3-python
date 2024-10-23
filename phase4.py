import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from phase3 import clear_image_folder, download_images
from phase2 import get_category_products_data, save_to_csv

INDEX_URL = "https://books.toscrape.com/"


def get_categories():
    response = requests.get(INDEX_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get all div.side_categories > ul > li > ul > li > a
    categories = []
    for category in (
        soup.find("div", class_="side_categories")
        .find_all("ul", recursive=True)[1]
        .find_all("li", recursive=False)
    ):
        categories.append(urljoin(INDEX_URL, category.a["href"]))

    return categories


def get_category_title(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Convert title to "Sentence Case" to "underline_case"
    title = soup.find("h1").string.replace(" ", "_").lower()
    # Remove all characters that are not alphanumeric
    title = "".join(char for char in title if (char.isalnum() or char == "_"))

    return title


if __name__ == "__main__":
    categories = get_categories()
    clear_image_folder()
    for category in categories:
        products_data = get_category_products_data(category)
        category_title = get_category_title(category)

        for product in products_data:
            download_images(product, "images/" + category_title)

        save_to_csv(products_data, f"product_data_{category_title}.csv")
        print(f"Data extracted and saved to product_data_{category_title}.csv")

    print("Data extracted and saved to product_data.csv")
