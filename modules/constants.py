# The urls for categories.
FEEDS = {
    "top": "https://khabarfarsi.com/rss/top",
    "politics": "https://khabarfarsi.com/rss/category/2470",
    "economy": "https://khabarfarsi.com/rss/category/2471",
    "society": "https://khabarfarsi.com/rss/category/2511",
    "culture": "https://khabarfarsi.com/rss/category/2512",
    "health": "https://khabarfarsi.com/rss/category/2513",
    "technology": "https://khabarfarsi.com/rss/category/2514",
    "international": "https://khabarfarsi.com/rss/category/2515",
    "religious": "https://khabarfarsi.com/rss/category/2516",
    "accidents": "https://khabarfarsi.com/rss/category/2517",
    "sports": "https://khabarfarsi.com/rss/category/2518",
}

# Make category user friendly
CATEGORY_LABELS = {
    "top": "برترین ها",
    "politics": "سیاسی",
    "economy": "اقتصادی",
    "society": "اجتماعی",
    "culture": "فرهنگی",
    "health": "سلامت",
    "technology": "فناوری",
    "international": "بین الملل",
    "religious": "مذهبی",
    "accidents": "حوادث",
    "sports": "ورزشی",
}


def category_label(key: str) -> str:
    return CATEGORY_LABELS.get(key, key)
