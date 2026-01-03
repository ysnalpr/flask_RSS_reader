import sqlite3, feedparser, re
from bs4 import BeautifulSoup


# Create and initialize the database
def init_db():
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        description TEXT, 
        image_url TEXT)"""
    )

    conn.commit()
    conn.close()


# Save news items to the database
def save_news_to_db(news_items):
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    for item in news_items:
        c.execute(
            """INSERT OR IGNORE INTO news (title, link, description, image_url) VALUES (?, ?, ?, ?)""",
            (item["title"], item["link"], item["description"], item["image_url"]),
        )

    conn.commit()
    conn.close()


# Fetch RSS feed and return news items
def fetch_rss_feed():
    url = "https://khabarfarsi.com/rss/top"
    feed = feedparser.parse(url)
    news_items = []

    for item in feed.entries:
        news_item = {
            "title": item.title,
            "link": item.link,
            "description": item.description,
            "image_url": None,
        }

        # Extract image URL from description if available
        soup = BeautifulSoup(item.description, "html.parser")
        image_tag = soup.find("img")

        if image_tag:
            image_url = image_tag.get("src")
            if image_url:
                news_item["image_url"] = image_url
                # print(image_url)

        news_items.append(news_item)

    return news_items
