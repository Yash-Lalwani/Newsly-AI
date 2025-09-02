from textblob import TextBlob
from urllib.parse import quote_plus
import feedparser
import datetime
from dateutil import parser


# This function builds the RSS URL for the searched keyword
def build_google_news_rss_url(keyword: str) -> str:
    q = quote_plus(keyword.strip())
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"


# This function analyzes the sentiment of the text as Positive, Negative, or Neutral
def get_sentiment(text: str) -> tuple:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "😊 Positive", "sentiment-positive"
    elif polarity < 0:
        return "😞 Negative", "sentiment-negative"
    else:
        return "😐 Neutral", "sentiment-neutral"


# This function fetches the source icon to display on the frontend for better UI
def get_source_icon(title: str) -> str:
    if "BBC" in title.upper():
        return "BBC"
    elif "CNN" in title.upper():
        return "CNN"
    elif "FOX" in title.upper():
        return "FOX"
    elif "REUTERS" in title.upper():
        return "RUT"
    elif "AP" in title.upper():
        return "AP"
    else:
        return "GGL"


# This function formats the time as a 'time ago' string for cleaner display
# Applying this function to the date allows us to show time as x days/hours ago
def format_time_ago(published_str: str) -> str:
    try:
        pub_date = parser.parse(published_str)
        now = datetime.datetime.now(pub_date.tzinfo)
        diff = now - pub_date

        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
    except:
        return "Recently"


# This function implements the chat feature on the app frontend.
# It works only if the user enters a news keyword starting with the query "find news on ".
# The function trims the prefix and returns only the keyword to pass to the search_news function
def parse_news_query(query: str) -> str:
    query = query.strip()
    if query.lower().startswith("find news on "):
        keywords = query[13:].strip()  # Remove "find news on " prefix
        return keywords if keywords else None  # Return None if no keywords remain
    return None


# This function fetches news articles for a given keyword using Google's RSS feed.
# It builds the RSS URL, parses the feed, and extracts the title, link, and published time
# (formatted as "x days/hours/minutes ago") for up to `max_results` articles.
# Returns a list of dictionaries with this information, or an empty list on error.
def search_news_for_chat(keywords: str, max_results: int = 3) -> list:
    try:
        url = build_google_news_rss_url(keywords)
        feed = feedparser.parse(url)

        articles = []
        for entry in feed.entries[:max_results]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "time_ago": format_time_ago(entry.get("published", ""))
            })

        return articles
    except Exception as e:
        return []