import streamlit as st
import feedparser
from components import (
    load_custom_css, render_header, render_hero, render_tabs,
    render_search_section, render_article_card
)
from news_utils import (
    build_google_news_rss_url, get_sentiment, get_source_icon, format_time_ago
)
from visualizations import render_insights_section
from chat_bot import render_chat_section


# Configure the page with title, favicon, and layout settings
# → This sets how the Streamlit app will look in the browser (title, icon, sidebar state, etc.)
st.set_page_config(
    page_title="Newsly.AI - AI Powered News Platform with Sentiment Analysis",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS styling to override Streamlit’s default look
# → The function loads an external stylesheet so the app has a polished UI.
load_custom_css()


# Main entry point of the app – calls all UI sections and handles logic
def main():
    # Render header section at the top
    # → Displays the app’s title, branding, or navigation.
    render_header()

    # Render hero/banner section
    # → Usually a big highlighted area with app description or tagline.
    render_hero()

    # Render navigation tabs (e.g., categories)
    # → Lets users switch between topics like Tech, Sports, etc.
    selected_category = render_tabs()

    # Render search input area
    # → Provides the search bar where users type keywords.
    render_search_section()

    # Create three side-by-side input boxes for keywords
    # → User can enter up to 3 topics (e.g., AI, Crypto, Elon Musk).
    col1, col2, col3 = st.columns(3)
    with col1:
        kw1 = st.text_input("", placeholder="e.g. Cryptocurrency", label_visibility="collapsed", key="kw1")
    with col2:
        kw2 = st.text_input("", placeholder="e.g. Artificial Intelligence", label_visibility="collapsed", key="kw2")
    with col3:
        kw3 = st.text_input("", placeholder="e.g. elon musk", label_visibility="collapsed", key="kw3")

    # Collect only non-empty keywords and build their Google News RSS URLs
    # → Converts user keywords into API-ready search links.
    keywords = [k.strip() for k in [kw1, kw2, kw3] if k.strip()]
    rss_urls = [build_google_news_rss_url(k) for k in keywords]

    # Add a “Fetch Headlines” button in the center
    # → When clicked, it triggers fetching articles from Google News.
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        st.write("")
        fetch_btn = st.button("🔍 Fetch Latest Headlines", type="primary")

    # Advanced search options (hidden inside an expander)
    # → Lets user customize number of articles, sorting, and sentiment filters.
    with st.expander("Advanced Options"):
        max_articles = st.slider("Maximum articles to display", 5, 20, 10)
        sort_by = st.selectbox("Sort by", ["Published Date", "Relevance", "Sentiment"])
        show_only = st.multiselect("Show only", ["Positive", "Negative", "Neutral"], default=["Positive", "Negative", "Neutral"])

    # If user clicked "Fetch" and provided keywords → start fetching news
    if fetch_btn and rss_urls:
        # Show a section header for results
        # → Uses custom HTML/CSS for a styled title above articles.
        st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h2 style="color: #e8eaed; font-size: 32px; font-weight: 700; margin-bottom: 8px;">📰 Latest Headlines</h2>
            <p style="color: #9aa0a6; font-size: 18px; margin: 0;">Top news articles with AI-powered sentiment analysis</p>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Fetching latest news..."):  # Show loading animation
            all_articles = []

            # For each keyword, fetch RSS feed and parse news articles
            # → Extracts title, link, date, and runs AI sentiment analysis.
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
                # Apply sentiment filters chosen by user
                # → Only show Positive, Negative, or Neutral articles if selected.
                sentiment_map = {"Positive": "😊 Positive", "Negative": "😞 Negative", "Neutral": "😐 Neutral"}
                if show_only:
                    selected_sentiments = [sentiment_map[s] for s in show_only]
                    all_articles = [a for a in all_articles if a["sentiment"] in selected_sentiments]

                # Sort articles by date or sentiment
                # → Ensures the most relevant/desired results are shown first.
                if sort_by == "Published Date":
                    all_articles.sort(key=lambda x: x["published"], reverse=True)
                elif sort_by == "Sentiment":
                    sentiment_order = {"😊 Positive": 0, "😐 Neutral": 1, "😞 Negative": 2}
                    all_articles.sort(key=lambda x: sentiment_order.get(x["sentiment"], 3))

                top_articles = all_articles[:max_articles]

                # Display quick statistics about fetched articles
                # → Shows total count and sentiment breakdown using metrics.
                if all_articles:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Articles", len(all_articles))
                    with col2:
                        positive_count = len([a for a in all_articles if "Positive" in a["sentiment"]])
                        st.metric("Positive", positive_count)
                    with col3:
                        negative_count = len([a for a in all_articles if "Negative" in a["sentiment"]])
                        st.metric("Negative", negative_count)
                    with col4:
                        neutral_count = len([a for a in all_articles if "Neutral" in a["sentiment"]])
                        st.metric("Neutral", neutral_count)

                    st.markdown("---")

                # Display featured and regular articles in a nice layout
                # → First 3 articles are highlighted, rest shown below.
                if len(top_articles) >= 3:
                    st.markdown("### Featured Articles")

                    render_article_card(top_articles[0], is_featured=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        render_article_card(top_articles[1])
                    with col2:
                        render_article_card(top_articles[2])

                    if len(top_articles) > 3:
                        st.markdown("### More Headlines")
                        for article in top_articles[3:]:
                            render_article_card(article)
                else:
                    for article in top_articles:
                        render_article_card(article)

                # Show extra insights/visualizations after the articles
                # → Could include charts like sentiment distribution.
                st.markdown("---")
                render_insights_section(top_articles)
            else:
                st.warning("No articles found. Please try different keywords.")

    elif fetch_btn:
        # User clicked fetch but gave no keywords
        # → Show warning instead of fetching empty search.
        st.warning("Please enter at least one keyword to search for news.")

    # Add chatbot at the bottom of the page
    # → Allows users to interact and ask questions about the news.
    render_chat_section()


# Run the app if this file is executed directly
if __name__ == "__main__":
    main()