from flask import Flask, render_template, request, redirect, url_for
from db import init_db, save_news_to_db, fetch_all_feeds
from modules import category_label
import sqlite3
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(
    app, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 60}
)  # 60 seconds


# Fetch and store news before each request
@app.before_request
def fetch_and_store_news():
    init_db()
    news_items = fetch_all_feeds()
    save_news_to_db(news_items)


# Helper function to build pagination links
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
@cache.cached(timeout=60, query_string=True)
def home():
    # Pagination parameters to get 9 items per page
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str).strip()
    category = request.args.get("category", "", type=str).strip()

    per_page = 9
    offset = (page - 1) * per_page

    # Database connection
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    # Categories for UI
    c.execute(
        "SELECT DISTINCT category FROM news WHERE category IS NOT NULL AND category != '' ORDER BY category"
    )
    categories = [row[0] for row in c.fetchall()]

    where = []
    params = []

    if q:
        where.append("(title LIKE ? OR description LIKE ?)")
        like = f"%{q}%"
        params.extend([like, like])

    if category:
        where.append("category = ?")
        params.append(category)

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""

    c.execute(
        f"SELECT * FROM news {where_sql} ORDER BY id DESC LIMIT ? OFFSET ?",
        (*params, per_page, offset),
    )
    news_items = c.fetchall()

    c.execute(
        f"SELECT COUNT(*) FROM news {where_sql}",
        (*params,),
    )
    total_items = c.fetchone()[0]

    conn.close()

    # Calculate total number of pages
    total_pages = max(1, (total_items + per_page - 1) // per_page)

    pagination = build_pagination(page, total_pages, window=2)
    return render_template(
        "index.html",
        news=news_items,
        page=page,
        total_pages=total_pages,
        pagination=pagination,
        q=q,
        category=category,
        categories=categories,
        category_label=category_label,
    )


@app.route("/detail/<int:news_id>")
def news_detail(news_id):
    conn = sqlite3.connect("news.db")
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE id = ?", (news_id,))
    item = c.fetchone()
    conn.close()

    if item:
        return render_template("detail.html", item=item)
    else:
        return "News not found!", 404


# Refresh button url
@app.route("/refresh")
def refresh():
    news_items = fetch_all_feeds()
    save_news_to_db(news_items)

    cache.clear()

    # Go back to where the user was
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    category = request.args.get("category", "", type=str)

    return redirect(url_for("home", page=page, q=q, category=category, refreshed=1))


if __name__ == "__main__":
    app.run(debug=True)
