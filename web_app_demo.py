from data_columns import column_names
import pandas as pd
import streamlit as st
from probabilistic_summarizer import summarize_news

# Load and process data
data = pd.read_csv("GDELT Event Files/20240806.export.CSV", sep="\t", header=None)
data.columns = column_names
clean_data = data.drop_duplicates(subset='source_url')
relevant_data = clean_data[['num_sources', 'source_url', 'goldstein_scale']]
sorted_data = relevant_data.sort_values(by='num_sources', ascending=False)
print(sorted_data.head(3))
# Get top 3 source URLs
urls = sorted_data.head(3).source_url.values.tolist()
# Generate summaries
summaries = [summarize_news(url) for url in urls]

# Create the Streamlit app
# Create the Streamlit app
st.title('Top 3 Most Mentioned News Articles')

# Create a container for the scrollable area
with st.container():
    for i, (url, summary) in enumerate(zip(urls, summaries), 1):
        # Extract title from the URL (you might want to improve this based on your actual data)
        title = f"Article {i}: {url.split('/')[-1]}"
        
        # Create an expander for each article
        with st.expander(title):
            st.write(summary)

# Add some CSS to make the container scrollable
st.markdown("""
    <style>
        .stContainer {
            max-height: 400px;
            overflow-y: auto;
        }
    </style>
    """, unsafe_allow_html=True)