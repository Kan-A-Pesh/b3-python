from bs4 import BeautifulSoup
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from phase4 import get_category_products_data, get_categories
from io import StringIO
import numpy as np


def get_raw_category_title(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("h1").string


def convert_category_pie(titles, data):
    pie_sizes = [len(data) for data in category_data]

    fig, ax = plt.subplots()
    ax.autoscale()
    ax.set_aspect("equal")
    ax.set_title("Percentage of Products in Each Category")

    ax.pie(pie_sizes, labels=category_titles)

    return fig


def convert_prices_pie(titles, data):
    prices = [
        sum([product["price_including_tax"] for product in category_data])
        / len(category_data)
        for category_data in data
    ]

    x = 0.5 + np.arange(len(prices) + 1)

    fig, ax = plt.subplots()
    ax.autoscale()
    ax.set_aspect("equal")
    ax.set_title("Average Price of Products in Each Category")

    ax.bar(x, prices, width=1, edgecolor="white", linewidth=0.7)

    ax.set(
        xlim=(0, 8),
        xticks=np.arange(1, len(prices) + 1),
        ylim=(0, 8),
        yticks=np.arange(1, len(prices) + 1),
    )

    return fig


def save_fig(fig, filename):
    fig.savefig(filename, bbox_inches="tight")


if __name__ == "__main__":
    categories = get_categories()
    category_titles = [get_raw_category_title(category) for category in categories]
    category_data = [get_category_products_data(category) for category in categories]

    convert_category_pie(category_titles, category_data).savefig(
        "categories.png", bbox_inches="tight"
    )
    convert_prices_pie(category_titles, category_data).savefig(
        "prices.png", bbox_inches="tight"
    )

    print("Charts saved to categories.pdf and prices.pdf")
