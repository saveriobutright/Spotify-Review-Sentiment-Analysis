from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright




def scrape_trustpilot(num_pages=10):
    all_reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(1, num_pages + 1):
            url = f"https://www.trustpilot.com/review/www.spotify.com?page={i}"
            print(f"Scraping page {i}...")
            
            page.goto(url, wait_until="networkidle")
            content = page.content()

            soup = BeautifulSoup(content, "html.parser")
            articles = soup.find_all("article")

            for article in articles:
                text_element = article.find("p", attrs={"data-service-review-text-typography": "true"})
                rating_element = article.find("div", attrs={"data-service-review-rating": True})

                text = text_element.get_text(strip=True) if text_element else None
                rating = rating_element["data-service-review-rating"] if rating_element else None

                if text and rating:
                    all_reviews.append({"Review": text, "Rating": int(rating)})

        browser.close()
                                                      
    return pd.DataFrame(all_reviews)


df = scrape_trustpilot(num_pages=10)
df = df.drop_duplicates(subset=["Review"])

print(f"\nScraped {len(df)} unique reviews.")

df["Rating"] = df["Rating"].astype(int)
print(df)
df.to_csv("data/raw_reviews.csv", index=False)
print("Data saved to data/raw_reviews.csv!")

