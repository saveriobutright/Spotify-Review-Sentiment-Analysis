from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright


url = "https://www.trustpilot.com/review/www.spotify.com"


def scrape_trustpilot(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        content = page.content()
        browser.close()
                                                    
    soup = BeautifulSoup(content, "html.parser")
    reviews = []
    articles = soup.find_all("article")
    for article in articles:
        text_element = article.find("p", attrs={"data-service-review-text-typography": "true"})
        rating_element = article.find("div", attrs={"data-service-review-rating": True})
        if text_element:
            text = text_element.get_text(strip=True)
        else:
            text = None
        if rating_element:
            rating = rating_element["data-service-review-rating"]
        else:
            rating = None

        if text:
            reviews.append({"Review": text, "Rating": rating})

    return pd.DataFrame(reviews)


df = scrape_trustpilot(url)
print(df)

df["Rating"] = df["Rating"].astype(int)
df.to_csv("data/raw_reviews.csv", index=False)
print("Data saved to data/raw_reviews.csv!")

