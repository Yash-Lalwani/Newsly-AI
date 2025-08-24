import streamlit as st
from textblob import TextBlob
import streamlit_shadcn_ui as ui

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
