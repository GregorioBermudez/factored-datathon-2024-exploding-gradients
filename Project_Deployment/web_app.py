import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import datetime
from llm_summary import summarize_news_article
from title_extractor import extract_article_text

# Initialize Spark Session
spark = SparkSession.builder.appName("WebApp").getOrCreate()

# Create the Streamlit app
st.title('Top News Articles')

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

def date_selector():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_option = st.radio("Get news from:", ["Yesterday", "Choose dates"])
    if date_option == "Yersterday":
        return yesterday, yesterday
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", yesterday, max_value=yesterday)
        with col2:
            initial_end_date = min(yesterday, start_date)
            end_date = st.date_input("End date", initial_end_date, min_value=start_date, max_value=yesterday)
        date_difference = (end_date - start_date).days
        if date_difference > 31:
            st.error("Please select a date range of 31 days or fewer.")
            return None, None
        return start_date, end_date

# Calculate the date range
start_date, end_date = date_selector()

if start_date is None:
    pass
elif start_date == end_date:
    st.write(f"Fetching news from {start_date}")
else:
    st.write(f"Fetching news from {start_date} to {end_date}")

def get_urls_from_databricks(start_date, end_date, num_urls):
    gold_table_name = "gold_layer"
    df = spark.table(gold_table_name)
    
    df_filtered = df.filter(
        (col("Day") >= start_date) & 
        (col("Day") <= end_date)
    )
    
    top_urls = df_filtered.orderBy(col("Importance").desc()).limit(num_urls)
    return top_urls.select("SOURCEURL").rdd.flatMap(lambda x: x).collect()

if start_date and end_date:
    start_date = start_date.strftime("%Y%m%d")
    end_date = end_date.strftime("%Y%m%d")
    urls = get_urls_from_databricks(start_date, end_date, 100)

    # Generate summaries
    num_news = 0
    with st.container():
        for url in urls:
            if num_news >= 10:
                break
            title, summary, category = get_cached_summary(url)
            if title and summary and category:
                num_news += 1
                if selected_category == "All" or category == selected_category:
                    with st.expander(f"{category}: {title}"):
                        st.write(f'Summary: {summary}')
                        st.write(f'URL: {url}')