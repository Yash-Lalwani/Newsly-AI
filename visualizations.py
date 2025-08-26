import altair as alt
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import re
import streamlit as st
import io


def clean_text_for_analysis(text: str) -> str:
    """Clean text for better word analysis"""
    # Remove punctuation and special characters, leaving only words and spaces.
    # Replace multiple spaces with a single space, then lowercase everything
    # for consistency so the analysis treats "News" and "news" the same.
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower().strip()
    return text


def create_word_cloud(articles: list) -> plt.Figure:
    """Create a word cloud from article titles and snippets"""
    # Combine all article titles into one big string so the word cloud
    # can analyze word frequency across the entire dataset.
    all_text = " ".join([article['title'] for article in articles])

    # Clean the combined text to remove noise (punctuation, casing, etc.).
    clean_text = clean_text_for_analysis(all_text)

    # Generate the word cloud visualization.
    # Here we set custom styling (colors, background, stopwords, size)
    # so it looks good in dark mode and avoids filler words like "news".
    wordcloud = WordCloud(
        width=350,
        height=150,
        background_color='#303134',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10,
        stopwords={'said', 'says', 'news', 'report', 'reports', 'new', 'first', 'time', 'people', 'year', 'years', 'day', 'week', 'month', 'today', 'latest', 'breaking', 'update', 'updates'}
    ).generate(clean_text)

    # Render the word cloud as a Matplotlib figure.
    # `imshow` displays the word cloud, axis is hidden, and
    # background is styled to match the app's dark theme.
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    fig.patch.set_facecolor('#202124')

    return fig


def create_keyword_frequency_chart(articles: list) -> alt.Chart:
    """Create a horizontal bar chart of top keywords"""
    # Combine article titles into one string and clean it
    # so we can extract word frequency using CountVectorizer.
    all_text = " ".join([article['title'] for article in articles])
    clean_text = clean_text_for_analysis(all_text)

    # CountVectorizer extracts the most frequent words or word pairs (bigrams).
    # We also define a custom stopword list so common but unhelpful words are ignored.
    vectorizer = CountVectorizer(
        max_features=15,
        stop_words=[...],  # (custom long list of stopwords)
        ngram_range=(1, 2)
    )

    try:
        # Convert text into a word frequency matrix and map it to feature names.
        word_freq = vectorizer.fit_transform([clean_text])
        feature_names = vectorizer.get_feature_names_out()
        frequencies = word_freq.toarray()[0]

        # Create a DataFrame with words and their frequencies for plotting.
        word_freq_df = pd.DataFrame({
            'word': feature_names,
            'frequency': frequencies
        }).sort_values('frequency', ascending=True)

        # Build a horizontal bar chart with Altair.
        # The chart shows top keywords, styled with custom colors and dark theme.
        chart = alt.Chart(word_freq_df).mark_bar(color='#8ab4f8').encode(
            x=alt.X('frequency:Q', title='Frequency'),
            y=alt.Y('word:N', title='Keywords', sort='-x'),
            tooltip=['word:N', 'frequency:Q']
        ).properties(
            width=600,
            height=400,
            title=alt.TitleParams(
                text="Top Keywords in Headlines",
                fontSize=16,
                fontWeight='bold',
                color='#e8eaed'
            )
        ).configure_axis(
            labelColor='#e8eaed',
            titleColor='#e8eaed',
            gridColor='#5f6368'
        ).configure_view(
            fill='#303134',
            stroke='#5f6368'
        ).configure_title(
            color='#e8eaed'
        )

        return chart
    except Exception as e:
        # If no meaningful words are found, return a placeholder chart
        # so the app doesn’t crash and still shows a visual.
        empty_df = pd.DataFrame({'word': ['No keywords found'], 'frequency': [0]})
        return alt.Chart(empty_df).mark_bar().encode(
            x='frequency:Q',
            y='word:N'
        ).properties(width=600, height=200)


def create_sentiment_distribution_chart(articles: list) -> alt.Chart:
    """Create a bar chart showing sentiment distribution"""
    # Loop through articles and count how many are Positive, Neutral, or Negative.
    # Strip emojis so only the text labels are counted.
    sentiment_counts = {}
    for article in articles:
        sentiment = article['sentiment'].replace('😊 ', '').replace('😞 ', '').replace('😐 ', '')
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

    # Convert counts into a DataFrame for Altair plotting.
    sentiment_df = pd.DataFrame([
        {'Sentiment': sentiment, 'Count': count}
        for sentiment, count in sentiment_counts.items()
    ])

    # Define custom colors for each sentiment type (green=positive, grey=neutral, red=negative).
    color_scale = alt.Scale(
        domain=['Positive', 'Neutral', 'Negative'],
        range=['#34a853', '#9aa0a6', '#ea4335']
    )

    # Build a bar chart showing how many articles fall into each sentiment.
    chart = alt.Chart(sentiment_df).mark_bar().encode(
        x=alt.X('Sentiment:N', title='Sentiment'),
        y=alt.Y('Count:Q', title='Number of Articles'),
        color=alt.Color('Sentiment:N', scale=color_scale, legend=None),
        tooltip=['Sentiment:N', 'Count:Q']
    ).properties(
        width=400,
        height=300,
        title=alt.TitleParams(
            text="Sentiment Distribution",
            fontSize=16,
            fontWeight='bold',
            color='#e8eaed'
        )
    ).configure_axis(
        labelColor='#e8eaed',
        titleColor='#e8eaed',
        gridColor='#5f6368'
    ).configure_view(
        fill='#303134',
        stroke='#5f6368'
    ).configure_title(
        color='#e8eaed'
    )

    return chart


def render_insights_section(articles: list):
    """Render the insights section with all visualizations"""
    if not articles:
        return

    # Add a styled section header in the Streamlit app
    # with a title and subtitle for the Insights section.
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 20px 0;">
        <h2 style="color: #e8eaed; font-size: 28px; font-weight: 700; margin-bottom: 8px;">📊 Insights from Today's Headlines</h2>
        <p style="color: #9aa0a6; font-size: 16px; margin: 0;">Visual analysis of news content and sentiment patterns</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Word Cloud ---
    # Display the word cloud image inside Streamlit.
    # Save it temporarily in memory (BytesIO) and show it as an image widget.
    st.markdown("### 🌟 Word Cloud")
    st.markdown("Most frequently mentioned words across all headlines")

    try:
        fig = create_word_cloud(articles)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        buf.seek(0)
        st.image(buf, width=500)
        plt.close(fig)  # Close the figure to free up memory
    except Exception as e:
        st.error(f"Error creating word cloud: {str(e)}")

    # --- Split into two columns for Keywords and Sentiment charts ---
    col1, col2 = st.columns(2)

    with col1:
        # Display the keyword frequency bar chart.
        st.markdown("### 📈 Top Keywords")
        st.markdown("Most common words and phrases in headlines")
        try:
            keyword_chart = create_keyword_frequency_chart(articles)
            st.altair_chart(keyword_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating keyword chart: {str(e)}")

    with col2:
        # Display sentiment distribution (positive, neutral, negative).
        st.markdown("### 🎭 Sentiment Analysis")
        st.markdown("Distribution of positive, neutral, and negative coverage")
        try:
            sentiment_chart = create_sentiment_distribution_chart(articles)
            st.altair_chart(sentiment_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating sentiment chart: {str(e)}")