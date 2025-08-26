import streamlit as st


# This function loads the style.css file into the app
def load_custom_css():
    with open('style.css', 'r') as f:
        css = f.read()

    st.markdown(f"""
    <style>
    {css}
    </style>
    """, unsafe_allow_html=True)


# Custom header created with CSS, including a logo and navigation
def render_header():
    st.markdown("""
    <div class="header-container">
        <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
            <div style="flex: 2; display: flex; align-items: center; color: #e8eaed; font-size: 24px; font-weight: 600;">
                <div style="width: 32px; height: 32px; background-color: #8ab4f8; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; margin-right: 8px;">📰</div>
                Newsly.AI
            </div>
            <div style="flex: 3; text-align: center; color: #9aa0a6; font-weight: 500;">
                AI-Powered News Platform
            </div>
            <div style="flex: 2; text-align: right;">
                <button onclick="alert('Premium features coming soon!')"
                        style="background-color: #8ab4f8; color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 500;">
                    Get Premium
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Hero Section created with CSS for UI improvement, with main title and description
def render_hero():
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0;">
        <div class="hero-badge">
            <span>⚡</span>
            Powered by AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="text-align: center; font-size: 3.5rem; font-weight: 700; margin-bottom: 24px; color: #e8eaed; line-height: 1.1;">
        Catch the latest buzz with <span style="background-color: #1a73e8; padding: 4px 12px; border-radius: 8px; color: white;">AI-driven</span><br />
        news aggregator
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align: center; font-size: 20px; color: #9aa0a6; margin-bottom: 3rem; font-weight: 400;">
        Get the latest headlines with sentiment analysis in seconds.
    </p>
    """, unsafe_allow_html=True)


# Navigation Tabs section for categories of news.
# A loop goes through the tabs array and displays them using Streamlit's column layout.
def render_tabs():
    tabs = ["Home", "AI", "U.S.", "World", "Local",
            "Business", "Technology", "Sports", "Science", "Health"]

    # Use Streamlit's columns for layout
    cols = st.columns(len(tabs))

    for i, tab in enumerate(tabs):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    padding:8px 0;
                    text-align:center;
                    border-radius:8px;
                    background-color:#b0c2d1;
                    color:#333;
                    font-weight:500;
                    cursor:pointer;
                    transition: all 0.3s ease;
                ">
                    {tab}
                </div>
                """,
                unsafe_allow_html=True
            )


# Search section with title and description
def render_search_section():
    st.markdown("""
    <div class="search-card">
        <h2 style="font-size: 2rem; font-weight: 600; color: #e8eaed; margin-bottom: 16px; text-align: center;">Search Topics</h2>
        <p style="font-size: 18px; color: #9aa0a6; margin-bottom: 2rem; text-align: center;">
            Enter up to three keywords to discover the latest news
        </p>
    </div>
    """, unsafe_allow_html=True)


# Render an individual article card with styling
def render_article_card(article, is_featured=False):
    if is_featured:
        card_style = "font-size: 24px; font-weight: 700;"
        card_class = "article-card featured"
    else:
        card_style = "font-size: 18px; font-weight: 600;"
        card_class = "article-card"

    # Truncate title if it's too long for non-featured articles
    title = article['title']
    if not is_featured and len(title) > 80:
        title = title[:80] + "..."

    st.markdown(f"""
    <div class="{card_class}">
        <a href="{article['link']}" target="_blank" style="color: #e8eaed; text-decoration: none; {card_style} display: block; margin-bottom: 12px; line-height: 1.4;">
            {title}
        </a>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 14px; color: #9aa0a6;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="background-color: #1a73e8; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600;">
                    {article['source_icon']}
                </div>
                <span>Keyword: {article['keyword']}</span>
            </div>
            <span>•</span>
            <span>{article['time_ago']}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <span class="{article['sentiment_class']}">{article['sentiment']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    