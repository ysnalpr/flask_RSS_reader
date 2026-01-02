from flask import Flask, render_template, request
from db import init_db, save_news_to_db, fetch_rss_feed
import sqlite3

app = Flask(__name__)


@app.before_request
def fetch_and_store_news():
    init_db()
    news_items = fetch_rss_feed()
    save_news_to_db(news_items)


def build_pagination(page, total_pages, window=2):
    if total_pages <= 1:
        return [1]

    pages = [1]
    start = max(2, page - window)
    end = min(total_pages - 1, page + window)

    if start > 2:
        pages.append(None)

    pages.extend(range(start, end + 1))

    if end < total_pages - 1:
        pages.append(None)

    pages.append(total_pages)
    return pages


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

    pagination = build_pagination(page, total_pages, window=2)
    return render_template(
        "index.html",
        news=news_items,
        page=page,
        total_pages=total_pages,
        pagination=pagination,
    )


if __name__ == "__main__":
    app.run(debug=True)
