from flask import Flask, render_template
from db import init_db, save_news_to_db, fetch_rss_feed
import sqlite3

app = Flask(__name__)


@app.before_request
def fetch_and_store_news():
    init_db()
    news_items = fetch_rss_feed()
    save_news_to_db(news_items)


@app.route("/")
def home():
    conn = sqlite3.connect("news.db")
    c = conn.cursor()
    c.execute("SELECT * FROM news ORDER BY id DESC")
    news_items = c.fetchall()
    conn.close()
    return render_template("index.html", news=news_items)


if __name__ == "__main__":
    app.run(debug=True)
