from flask import Flask, render_template, request
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
    # Pagination parameters to get 10 items per page
    page = request.args.get("page", 1, type=int)
    per_page = 9
    offset = (page - 1) * per_page

    # Database connection
    conn = sqlite3.connect("news.db")
    c = conn.cursor()
    # Get paginated news from database
    c.execute(
        "SELECT * FROM news ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset)
    )
    news_items = c.fetchall()

    # Get total number of items from database
    c.execute("SELECT COUNT(*) FROM news")
    total_items = c.fetchone()[0]

    conn.close()
    # Calculate total number of pages
    total_pages = (total_items + per_page - 1) // per_page
    return render_template(
        "index.html",
        news=news_items,
        page=page,
        total_pages=total_pages,
    )


if __name__ == "__main__":
    app.run(debug=True)
