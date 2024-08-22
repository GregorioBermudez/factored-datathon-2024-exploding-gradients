from data_columns import column_names
import pandas as pd
import datetime

def clean_dataframe(df):
    """
    Cleans the given dataframe by performing the following operations:
    1. Group the dataframe by 'source_url' column.
    2. Calculate the mean of the following columns: 'num_sources', 'avg_tone', 'goldstein_scale', 'num_articles'.
    3. Return the cleaned dataframe.

    Parameters:
    - df: pandas.DataFrame
        The input dataframe to be cleaned.

    Returns:
    - pandas.DataFrame
        The cleaned dataframe.
    """
    clean_data = df.copy()
    clean_data = clean_data.groupby('source_url', as_index = False).agg({
        'num_sources': 'mean',
        'avg_tone': 'mean',
        'goldstein_scale' : 'mean',
        'num_articles': 'mean',
        'goldstein_scale': 'mean',
        'avg_tone': 'mean'
        })
    return clean_data

def get_relevant_data(date):
    """
    Retrieves relevant data for a given date.

    Parameters:
    date (str): The date in the format 'YYYY-MM-DD'.

    Returns:
    pandas.DataFrame: The cleaned and relevant data for the given date.
    """
    data = pd.read_csv(f"Data_Storage/GDELT Event Files/{date}.export.CSV", sep="\t", header=None)
    data.columns = column_names
    relevant_data = clean_dataframe(data)
    return relevant_data

def get_sorted_data(data, num_urls):
    """
    Sorts the given data based on the importance score and returns the top 'num_urls' rows.

    Parameters:
    - data: DataFrame
        The input data containing the relevant information.
    - num_urls: int
        The number of URLs to return.

    Returns:
    - DataFrame
        The sorted data with the top 'num_urls' rows based on the importance score.
    """
    relevant_data = data.copy()
    relevant_data['importance'] = relevant_data['num_sources']/max(relevant_data['num_sources']) + abs(relevant_data['avg_tone']/max(abs(relevant_data['avg_tone']))) 
    return relevant_data.sort_values(by='importance', ascending=False).head(num_urls)

def get_urls(start_date, end_date, num_urls):
    """
    Retrieves a list of URLs based on the given start date, end date, and number of URLs.

    Parameters:
    - start_date (datetime): The start date for retrieving relevant data.
    - end_date (datetime): The end date for retrieving relevant data.
    - num_urls (int): The number of URLs to be returned.

    Returns:
    - urls (list): A list of URLs sorted based on the retrieved data.

    """
    if start_date == end_date:
        date = start_date.strftime("%Y%m%d")
        relevant_data = get_relevant_data(date)
        sorted_data = get_sorted_data(relevant_data, num_urls)
        urls = sorted_data.source_url.values.tolist()
        return urls
    else:
        all_dfs = []
        days = (end_date - start_date).days
        date = start_date.strftime("%Y%m%d")
        for i in range(days):
            date = (start_date + datetime.timedelta(days=i)).strftime("%Y%m%d")
            relevant_data = get_relevant_data(date)
            all_dfs.append(relevant_data)
        data = pd.concat(all_dfs)
        sorted_data = get_sorted_data(data, num_urls)
        urls = sorted_data.source_url.values.tolist()
        return urls