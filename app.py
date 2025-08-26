import streamlit as st
from textblob import TextBlob
import streamlit_shadcn_ui as ui
from urllib.parse import quote_plus
import feedparser
import datetime
from dateutil import parser
from articles_template import generate_articles_html


# Configure the page
st.set_page_config(
    page_title="Newsly.AI - AI Powered News Platform with Sentiment Analysis",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# # Load external CSS
def local_css(file_name):
    with open(file_name) as fn:
        st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Load header section from external file
def load_header_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

header = load_header_html("header.html")
st.markdown(header, unsafe_allow_html=True)

# Load hero section from external file
def load_hero_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

hero = load_hero_html("hero.html")
st.markdown(hero, unsafe_allow_html=True)

# Load tabs section from external file
def load_tabs_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

tabs = load_tabs_html("tabs.html")
st.markdown(tabs, unsafe_allow_html=True)

# Load results header section from external file
def load_results_header_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

# Helper functions
def build_google_news_rss_url(keyword: str) -> str:
    q = quote_plus(keyword.strip())
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"

def get_sentiment(text: str) -> tuple:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "😊 Positive", "sentiment-positive"
    elif polarity < 0:
        return "😞 Negative", "sentiment-negative"
    else:
        return "😐 Neutral", "sentiment-neutral"
    
def get_source_icon(title: str) -> str:
    if "BBC" in title.upper():
        return "BBC"
    elif "CNN" in title.upper():
        return "CNN"
    elif "FOX" in title.upper():
        return "FOX"
    elif "REUTERS" in title.upper():
        return "R"
    elif "AP" in title.upper():
        return "AP"
    else:
        return "N"

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
    
# Search section
def load_search_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

search = load_search_html("search.html")
st.markdown(search, unsafe_allow_html=True)


# Keyword inputs
col1, col2, col3 = st.columns(3)
with col1:
    kw1 = st.text_input("", placeholder="e.g. Cryptocurrency", label_visibility="collapsed", key="kw1")
with col2:
    kw2 = st.text_input("", placeholder="e.g. Artificial Intelligence", label_visibility="collapsed", key="kw2")
with col3:
    kw3 = st.text_input("", placeholder="e.g. elon musk", label_visibility="collapsed", key="kw3")

# Collect keywords
keywords = [k.strip() for k in [kw1, kw2, kw3] if k.strip()]
rss_urls = [build_google_news_rss_url(k) for k in keywords]

# Create 3 columns, middle one holds the button
col1, col2, col3, col4, col5 = st.columns(5)

with col3:
    st.write("")
    fetch_btn = st.button("🔍 Fetch Latest Headlines", type="primary")

if fetch_btn and rss_urls:
    # Results section header
    results_header_html = load_results_header_html("results_header.html")
    st.markdown(results_header_html, unsafe_allow_html=True)
    
    with st.spinner("Fetching latest news..."):
        all_articles = []
        
        # Parse feeds for each keyword
        for kw, url in zip(keywords, rss_urls):
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    sentiment_text, sentiment_class = get_sentiment(entry.title)
                    article = {
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", "No date"),
                        "keyword": kw,
                        "sentiment": sentiment_text,
                        "sentiment_class": sentiment_class,
                        "source_icon": get_source_icon(entry.title),
                        "time_ago": format_time_ago(entry.get("published", ""))
                    }
                    all_articles.append(article)
            except Exception as e:
                st.error(f"Error fetching news for '{kw}': {str(e)}")
        
        if all_articles:
            # Sort by published date
            all_articles.sort(key=lambda x: x["published"], reverse=True)
            top_articles = all_articles[:10]
            
            # Generate articles HTML using template
            articles_html = generate_articles_html(top_articles)
            st.markdown(articles_html, unsafe_allow_html=True)
        else:
            st.warning("No articles found. Please try different keywords.")

elif fetch_btn:
    st.warning("Please enter at least one keyword to search for news.")
    