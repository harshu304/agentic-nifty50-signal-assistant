import feedparser

def fetch_news(stock_name="NIFTY"):
    url = f"https://news.google.com/rss/search?q={stock_name}+stock"

    feed = feedparser.parse(url)

    headlines = [entry.title for entry in feed.entries[:5]]

    return headlines