from data_columns import column_names
import pandas as pd
import streamlit as st

data = pd.read_csv("GDELT Event Files/20240806.export.CSV", sep= "\t", header = None)
data.columns = column_names

relevant_data= data[['goldstein_scale','avg_tone','day','source_url', 'actor1_geo_full_name']]

# Count occurrences of each country
country_counts = relevant_data['actor1_geo_full_name'].value_counts()

# Filter countries mentioned more than 7 times
frequent_countries = country_counts[country_counts > 7].index

# Create a new dataframe with only frequent countries
filtered_df = relevant_data[relevant_data['actor1_geo_full_name'].isin(frequent_countries)]

countries_avg_goldstein = filtered_df.groupby('actor1_geo_full_name')['goldstein_scale'].sum()

worse_10 = countries_avg_goldstein.sort_values(ascending=True).head(10)

# Create the Streamlit app
st.title('Top 10 Worse Countries by Sum Goldstein Scale')

# Display the bar chart
st.bar_chart(worse_10)