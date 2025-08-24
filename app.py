import streamlit as st
from textblob import TextBlob
import streamlit_shadcn_ui as ui
from urllib.parse import quote_plus
import feedparser
import datetime
from dateutil import parser


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
    results_header_html = """
    <div style="width: 100vw; margin-left: calc(-50vw + 50%); position: relative;">
        <section class="results-section">
            <div class="container">
                <h2 class="results-title">📰 Latest Headlines</h2>
                <p class="results-subtitle">Top news articles with AI-powered sentiment analysis</p>
            </div>
        </section>
    </div>
    """
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
            
            # Create full-width container for articles
            articles_html = """
            <div style="width: 100vw; margin-left: calc(-50vw + 50%); position: relative; padding: 0 0 60px 0;">
                <div class="container">
            """
            
            # Featured article layout (first 3 articles)
            if len(top_articles) >= 3:
                articles_html += '<div class="featured-grid">'
                
                # Main featured article
                main_article = top_articles[0]
                articles_html += f"""
                <div class="main-article">
                    <a href="{main_article['link']}" class="main-article-title" target="_blank">
                        {main_article['title']}
                    </a>
                    <div class="article-meta">
                        <div class="news-source">
                            <div class="source-icon">{main_article['source_icon']}</div>
                            <span>Keyword: {main_article['keyword']}</span>
                        </div>
                        <span>•</span>
                        <span>{main_article['time_ago']}</span>
                    </div>
                    <div class="article-stats">
                        <span class="{main_article['sentiment_class']}">{main_article['sentiment']}</span>
                    </div>
                </div>
                """
                articles_html += '<div class="side-articles">'
                for article in top_articles[1:3]:
                    articles_html += f"""
                    <div class="side-article">
                        <a href="{article['link']}" class="side-article-title" target="_blank">
                            {article['title'][:80]}{'...' if len(article['title']) > 80 else ''}
                        </a>
                        <div class="article-meta">
                            <div class="news-source">
                                <div class="source-icon">{article['source_icon']}</div>
                                <span>{article['keyword']}</span>
                            </div>
                            <span>•</span>
                            <span>{article['time_ago']}</span>
                        </div>
                        <div class="article-stats">
                            <span class="{article['sentiment_class']}">{article['sentiment']}</span>
                        </div>
                    </div>
                    """
                
                articles_html += '</div></div>'  # Close side-articles and featured-grid
                
                # Remaining articles
                remaining_articles = top_articles[3:]
            else:
                remaining_articles = top_articles
            
            # Regular article cards
            for article in remaining_articles:
                articles_html += f"""
                <div class="article-card">
                    <a href="{article['link']}" class="article-title" target="_blank">
                        {article['title']}
                    </a>
                    <div class="article-meta">
                        <div class="news-source">
                            <div class="source-icon">{article['source_icon']}</div>
                            <span>Keyword: {article['keyword']}</span>
                        </div>
                        <span>•</span>
                        <span>{article['time_ago']}</span>
                    </div>
                    <div class="article-stats">
                        <span class="{article['sentiment_class']}">{article['sentiment']}</span>
                    </div>
                </div>
                """
            
            articles_html += """
                </div>  <!-- Close container -->
            </div>  <!-- Close full-width wrapper -->
            """
            
            st.markdown(articles_html, unsafe_allow_html=True)
        else:
            st.warning("No articles found. Please try different keywords.")

elif fetch_btn:
    st.warning("Please enter at least one keyword to search for news.")