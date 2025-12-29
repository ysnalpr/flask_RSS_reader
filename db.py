import sqlite3, feedparser


# Create and initialize the database
def init_db():
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        description TEXT)"""
    )

    conn.commit()
    conn.close()


# Save news items to the database
def save_news_to_db(news_items):
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    for item in news_items:
        c.execute(
            """INSERT INTO news (title, link, description) VALUES (?, ?, ?)""",
            (item["title"], item["link"], item["description"]),
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
        }
        news_items.append(news_item)

    return news_items
