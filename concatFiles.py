import pandas as pd
import glob

# Path to the folder containing the CSV files
csv_folder_path = r'GDELT Event Files'

# List of column names (replace with your actual column names)
csv_columns = ['global_id',
 'day', # Date the event took place in YYYYMMDD format
 'month_year', # Alternative formating YYYYMM
 'year', # Year
 'fraction_date', # Alternative formating YYYY.FFFF, where FFFF is the percentage of the year completed by that day
# actor 1
 'actor1_code',
 'actor1_name', # Name of Actor 1
 'actor1_country_code',
 'actor1_known_group_code', # Which group the actor belongs to NGO/ IGO/ rebel group. Ex: United Nations
 'actor1_ethnic_code',
 'actor1_religion1_code',
 'actor1_religion2_code',
 'actor1_type1_code', # Type codes talk about roles, for example police forces
 'actor1_type2_code', # goverment, military, education, elites, media, etc
 'actor1_type3_code', # -
# actor 2
 'actor2_code',
 'actor2_name', # Name of actor 2
 'actor2_country_code',
 'actor2_known_group_code',
 'actor2_ethnic_code',
 'actor2_religion1_code',
 'actor2_religion2_code',
 'actor2_type1_code', # Same as in actor 1
 'actor2_type2_code', # -
 'actor2_type3_code', # -
# ----------------
 'is_root_event', # Binary. Says if it is the root event. Can give insight into importance
 'event_code',
 'event_base_code',
 'event_root_code',
 'quad_class', # Event taxonomy: 1. Verbal cooperation, 2. Material Cooperation, 3. Verbal Conflict, 4. Material Conflict
 'goldstein_scale', # Numeric score from -10 to +10 capturing potential impact that the event will have in countries stability
 'num_mentions', # Number of mentions of the event across all documents. Can be seen as importance measure
 'num_sources', # Number of information sources containing mentions of the event
 'num_articles',# Number of source documents containing mentions of this event
 'avg_tone', # Avg tone of documents that mention the event. Goes from -100 (extremely negative) to 100 (extremely positive)
# actor 1 geo
 'actor1_geo_type', # Maps to: 1.Country, 2. US State, 3. US City, 4. World city, 5. World State
 'actor1_geo_full_name', # Name of location
 'actor1_geo_country_code',
 'actor1_geo_adm1_code',
 'actor1_geo_lat', # Latitude
 'actor1_geo_long', # Longitude
 'actor1_geo_feature_id',
# actor 2 geo
 'actor2_geo_type', # Check actor 1
 'actor2_geo_fullname',
 'actor2_geo_countrycode',
 'actor2_geo_adm1_code',
 'actor2_geo_lat',
 'actor2_geo_long',
 'actor2_geo_feature_id',
# action geo
 'action_geo_type', # Check actor 1
 'action2_geo_full_name',
 'action_geo_country_code',
 'action_geo_adm1_code',
 'action_geo_lat',
 'action_geo_long',
 'action_geo_feature_id',
# date and url
 'date_added', # Date the event was added to master database
 'source_url'] # URL

# Use glob to get all CSV files in the folder
all_files = glob.glob(csv_folder_path + "/*.csv")[100:200]

# Initialize an empty list to store DataFrames
df_list = []

# Iterate through the list of files and read each into a DataFrame
for filename in all_files:
    df = pd.read_csv(filename, header=None, names=csv_columns, sep="\t")
    df_list.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(df_list, ignore_index=True)

# Remove duplicates based on the "source_url" column
deduplicated_df = combined_df.drop_duplicates(subset="source_url")

# Save the deduplicated DataFrame to a single CSV file
output_path = "masterData2  .csv"
deduplicated_df.drop_duplicates(subset="source_url").to_csv(output_path, index=False)

print(f"Combined and deduplicated file saved to {output_path}")
