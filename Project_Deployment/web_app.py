import streamlit as st
import pandas as pd
from databricks import sql
import os
from datetime import datetime, timedelta
from llm_summary import summarize_news_article
from title_extractor import extract_article_text
import pytz
import plotly.express as px

# Databricks connection parameters
SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
ACCESS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# Create the Streamlit app
st.title('Top News Articles Around the World :earth_americas:')

# Use streamlit's caching mechanism
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def get_cached_summary(url):
    with st.spinner('Generating summary'):
        title = extract_article_text(url)
        summary, category = summarize_news_article(url)
        if summary is None or "unavailable" in title or "BizToc" in title:
            return None, None, None
        return title, summary, category

# Add a sidebar for category selection
st.sidebar.title("News Categories")
selected_category = st.sidebar.selectbox(
    "Select categories to display",
    ["All", "Political", "Economical", "Social"]
)

date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
st.write(f"Current date: {date_now}")
def date_selector():
    utc_now = datetime.now(pytz.utc)
    news_release_time = utc_now.replace(hour=10, minute=0, second=0, microsecond=0)
    yesterday = datetime.now().date() - timedelta(days=1)
    date_option = st.radio("Get news from:", ["Yesterday", "Choose dates"])
    
    if date_option == "Yesterday":
        if utc_now < news_release_time:
            st.warning("Yesterday's news will be released at 6:00 AM EST.")
            return None, None
        return yesterday, yesterday
    else:
        min_date = datetime(2023, 8, 13)
        before_yesterday = yesterday - timedelta(days=1)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", before_yesterday, min_value = min_date, max_value=yesterday)
        with col2:
            initial_end_date = min(before_yesterday, start_date)
            end_date = st.date_input("End date", initial_end_date, min_value=start_date, max_value=yesterday)
        date_difference = (end_date - start_date).days
        if date_difference > 31:
            st.error("Please select a date range of 31 days or fewer.")
            return None, None
        return start_date, end_date
        
# Calculate the date range
start_date, end_date = date_selector()
min_news = st.selectbox("Number of news articles to display", [5, 10, 15, 20, 25])
def get_urls_from_databricks(start_date, end_date, num_urls):
    with sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN
    ) as connection:
        with connection.cursor() as cursor:
            query = f"""
            SELECT SOURCEURL
            FROM gold_layer
            WHERE Day >= '{start_date.strftime("%Y%m%d")}' AND Day <= '{end_date.strftime("%Y%m%d")}'
            ORDER BY Importance DESC
            LIMIT {num_urls}
            """
            cursor.execute(query)
            result = cursor.fetchall()
    return [row[0] for row in result]

if start_date and end_date:
    if start_date == end_date:
        st.write(f"Fetching news from {start_date}")
    else:
        st.write(f"Fetching news from {start_date} to {end_date}")
    urls = get_urls_from_databricks(start_date, end_date, 100)

    # Generate summaries
    num_news = 0
    # Initialize counters and flags for each category
    categories = ["Political", "Economical", "Social"]
    category_found = {cat: False for cat in categories}
    category_count = {cat: 0 for cat in categories}
    category_found["All"] = True

    with st.container():
        for url in urls:
            if num_news >= min_news:
                break
            title, summary, category = get_cached_summary(url)
            if title and summary and category:
                num_news += 1
                if selected_category == "All" or category == selected_category:
                    category_found[category] = True
                    category_count[category] += 1
                    with st.expander(title):
                        st.write(f'Category: {category}')
                        st.write(f'Summary: {summary}')
                        st.write(f'URL: {url}')
    if not category_found[selected_category]:
        st.warning(f"No relevant {selected_category} news in the top {min_news} articles for the selected dates.")
    if selected_category == "All":
        # Create and display the plot
        st.subheader("News Category Distribution")
        
        # Prepare data for the plot
        plot_data = pd.DataFrame({
            'Category': categories,
            'Count': [category_count[cat] for cat in categories]
        })

        # Create the bar plot
        fig = px.bar(plot_data, x='Category', y='Count', 
                    title='Distribution of News Articles by Category',
                    labels={'Count': 'Number of Articles'},
                    color='Category')

        # Customize the layout
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Articles",
            showlegend=False
        )

        # Display the plot
        st.plotly_chart(fig)
