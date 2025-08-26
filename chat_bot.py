import streamlit as st
from news_utils import parse_news_query, search_news_for_chat

def render_chat_section():
    """This function creates a simple AI chat assistant that finds news articles."""

    # --- Section header with title and description ---
    st.markdown("---")  # Horizontal divider
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h3>💬 AI Chat Assistant</h3>
        <p>Ask me to find news on any topic!</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Chat history (stored in session_state to persist across refresh) ---
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []  # Initialize empty list for messages

    # --- Display previous messages from the chat history ---
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):  # Role can be "user" or "assistant"
            st.markdown(message["content"])

            # If assistant’s reply included articles, render them as clickable links
            if message["role"] == "assistant" and "articles" in message:
                for article in message["articles"]:
                    st.markdown(f"- [{article['title']}]({article['link']}) ({article['time_ago']})")

    # --- Chat input box for user messages ---
    user_input = st.chat_input("Example: Find news on Artificial Intelligence")

    if user_input:
        # Save the user’s message to session_state
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        # Show the user’s message in the chat window
        with st.chat_message("user"):
            st.markdown(user_input)

        # --- Step 1: Parse the query to extract keywords ---
        keywords = parse_news_query(user_input)

        if keywords:
            # --- Step 2: Search for news articles ---
            with st.chat_message("assistant"):
                with st.spinner("Looking for news..."):  # Loading spinner while fetching articles
                    articles = search_news_for_chat(keywords)

                if articles:
                    # Build assistant’s reply with results
                    reply_text = f"Here are some articles about **{keywords}**:"
                    st.markdown(reply_text)

                    for article in articles:
                        st.markdown(f"- [{article['title']}]({article['link']}) ({article['time_ago']})")

                    st.markdown("Hope this helps! 😊")

                    # Save assistant’s reply along with articles to session_state
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": reply_text + "\n\nHope this helps! 😊",
                        "articles": articles
                    })
                else:
                    # If no articles are found
                    error_msg = f"Sorry, I couldn't find any news on **{keywords}**."
                    st.markdown(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})

        else:
            # --- Step 3: Fallback if the query is not in the right format ---
            fallback_msg = "Please ask in the format: **'Find news on X'**. For example: 'Find news on climate change'."
            with st.chat_message("assistant"):
                st.markdown(fallback_msg)
            st.session_state.chat_messages.append({"role": "assistant", "content": fallback_msg})