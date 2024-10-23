import pathlib
import requests
from phase2 import get_category_products_data, save_to_csv

CATEGORY_URL = (
    "https://books.toscrape.com/catalogue/category/books/classics_6/index.html"
)


def clear_image_folder():
    # Remove images/ folder if it exists
    if pathlib.Path("images").exists():
        for file in pathlib.Path("images").iterdir():
            file.unlink()
        pathlib.Path("images").rmdir()

    # Create images/ folder
    pathlib.Path("images").mkdir(parents=True, exist_ok=True)


def download_images(product_data, location):
    # Create location folder if it doesn't exist
    pathlib.Path(location).mkdir(parents=True, exist_ok=True)

    # Convert title to "Sentence Case" to "underline_case"
    title = product_data["title"].replace(" ", "_").lower()

    # Remove all characters that are not alphanumeric
    title = "".join(char for char in title if (char.isalnum() or char == "_"))

    # Download image
    image_url = product_data["image_url"]
    image_response = requests.get(image_url)
    image_content = image_response.content
    image_path = pathlib.Path(location, f"{title}.jpg")
    image_path.write_bytes(image_content)

    return product_data


if __name__ == "__main__":
    clear_image_folder()
    products_data = get_category_products_data(CATEGORY_URL)
    for product in products_data:
        download_images(product, "images")
    save_to_csv(products_data)
    print("Data extracted and saved to product_data.csv")
