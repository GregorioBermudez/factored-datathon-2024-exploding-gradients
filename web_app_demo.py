from data_columns import column_names
import pandas as pd
import streamlit as st
from llm_summary import summarize_news_article
import datetime
from title_extractor import extract_article_text
from url_getter import get_urls



# Create the Streamlit app
# Create the Streamlit app
st.title('Top 3 Most Mentioned News Articles')

# Use streamlit's caching mechanism
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_summary(url):
    title = extract_article_text(url)
    summary, category = summarize_news_article(url)
    if summary == None:
        return None, None, None
    return title, summary, category

# Add a sidebar for category selection
st.sidebar.title("News Categories")
selected_category = st.sidebar.selectbox(
    "Select categories to display",
    ["Political", "Economical", "Social"]
    )
def date_selector():
    # Get today's date
    today = datetime.date.today()

    # Option to choose between today and date range
    date_option = st.radio("Get news from:", ["Today", "Choose dates"])

    if date_option == "Today":
        return today, today
    else:
        # Allow user to select start and end dates
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", today, max_value=today)
        with col2:
            # Ensure the initial end_date is not after today
            initial_end_date = min(today, start_date)
            end_date = st.date_input("End date", initial_end_date, min_value=start_date, max_value=today)

        # Calculate the difference between start and end dates
        date_difference = (end_date - start_date).days

        # Check if the range is within 31 days
        if date_difference > 31:
            st.error("Please select a date range of 31 days or fewer.")
            return None, None
        else:
            return start_date, end_date

# Calculate the date range
start_date, end_date = date_selector()
if start_date == None:
    pass
elif start_date == end_date:
    st.write(f"Fetching news from {start_date}")
else:
    st.write(f"Fetching news from {start_date} to {end_date}")
    
urls = get_urls(start_date, end_date, 10)
# Generate summaries

# Create a container for the scrollable area
with st.container():
    for url in urls:
        # Extract title from the URL (you might want to improve this based on your actual data)
        title, summary, category = get_cached_summary(url)
        if title != None and summary != None and category != None:
            if category in selected_category:
                # Create an expander for each article
                with st.expander(f"{category}: {title}"):
                    st.write(f'Summary: {summary}')
                    st.write(f'URL: {url}')

# Add some CSS to make the container scrollable
st.markdown("""
    <style>
        .stContainer {
            max-height: 400px;
            overflow-y: auto;
        }
    </style>
    """, unsafe_allow_html=True)