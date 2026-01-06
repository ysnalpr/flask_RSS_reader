import sqlite3, feedparser, re
from bs4 import BeautifulSoup
from modules import FEEDS


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
        image_url TEXT, 
        category TEXT)"""
    )

    conn.commit()
    conn.close()


# Save news items to the database
def save_news_to_db(news_items):
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    for item in news_items:
        c.execute(
            """INSERT OR IGNORE INTO news (title, link, description, image_url, category) VALUES (?, ?, ?, ?, ?)""",
            (
                item["title"],
                item["link"],
                item["description"],
                item["image_url"],
                item["category"],
            ),
        )

    conn.commit()
    conn.close()


def extract_image_url(html: str):
    soup = BeautifulSoup(html or "", "html.parser")
    img = soup.find("img")
    return img.get("src") if img else None


# Fetch RSS feed and return news items
def fetch_rss_feed(url: str, category: str):
    feed = feedparser.parse(url)
    news_items = []

    for item in feed.entries:
        description = getattr(item, "description", "")
        news_items.append(
            {
                "title": item.title,
                "link": item.link,
                "description": description,
                "image_url": extract_image_url(description),
                "category": category,
            }
        )

    return news_items


def fetch_all_feeds():
    all_items = []
    for category, url in FEEDS.items():
        all_items.extend(fetch_rss_feed(url, category))

    return all_items
