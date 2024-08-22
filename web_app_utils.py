from data_columns import column_names
import pandas as pd
import datetime
def get_urls(start_date, end_date, num_urls):
    if start_date == end_date:
        date = start_date.strftime("%Y%m%d")
        data = pd.read_csv(f"Data_Storage/GDELT Event Files/{date}.export.CSV", sep="\t", header=None)
        data.columns = column_names
        clean_data = data.drop_duplicates(subset='source_url')
        relevant_data = clean_data[['num_sources', 'source_url']]
        sorted_data = relevant_data.sort_values(by='num_sources', ascending=False).head(num_urls)
        urls = sorted_data.source_url.values.tolist()
        return urls
    else:
        all_dfs = []
        days = (end_date - start_date).days
        date = start_date.strftime("%Y%m%d")
        for i in range(days):
            date = (start_date + datetime.timedelta(days=i)).strftime("%Y%m%d")
            data = pd.read_csv(f"Data_Storage/DELT Event Files/{date}.export.CSV", sep="\t", header=None)
            data.columns = column_names
            clean_data = data.drop_duplicates(subset='source_url')
            relevant_data = clean_data[['num_sources', 'source_url']]
            all_dfs.append(relevant_data)
        data = pd.concat(all_dfs)
        sorted_data = data.sort_values(by='num_sources', ascending=False).head(num_urls)
        urls = sorted_data.source_url.values.tolist()
        return urls
