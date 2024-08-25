# Factored Datathon 2024 - Exploding Gradients

Check out our final deployed tool: 

## The Challege - News Analysis

Synthesize vast amounts of news data into insightful summaries that capture the essence of current events, helping stakeholders make informed decisions based on reliable and unbiased information Especifically, use Natural Language Processing (NLP) to create a summary of news for a specific period picking topics such as Social, Political, and Economical. General guidelines for the analysis: 

- Identify fake news to avoid using them as input 
- Minimize political polarization. Focus more on facts than opinions
- Include geographical and time dimensions within the analysis 

**Overll Goal**: Create insightful, unbiased summaries of current events to aid decision-making

## The Data

This challege is address using the [GDELT](https://www.gdeltproject.org) - Global Database of Events, Language,and Tone. Specifically, we used the GDELT 1.0 Global Knowledge Graph (GKG) and Events data. This
dataset provides a rich source of information on global events, news articles, and their
associated metadata, allowing us to analyze and derive insights from a wide range of
topics across various domains.

## The Team 

- Gregorio Bermúdez - Mathematical Engineering Student |[Linkedin](https://www.linkedin.com/in/gregorio-bermúdez-5a7b3a218/)| |[Github](https://github.com/GregorioBermudez)|
- Samuel Rico - Mathematical Engineering Student |[Linkedin](https://www.linkedin.com/in/samuel-rico/)| |[Github](https://github.com/sricog)|
- Santiago López - Mathematical Engineering Student |[Linkedin](https://www.linkedin.com/in/santiagolopezc/)| |[Github](https://github.com/Santilopezc)|
- Isabel Mora - Mathematical Engineering Student |[Linkedin](https://www.linkedin.com/in/isabel-mora-restrepo-a86031227/)| |[Github](https://github.com/isabelmorar)|

## The Solution 

### Data Storage and Data Cleaning

In this project, raw event data from the [GDELT](http://data.gdeltproject.org/events/index.html) dataset was processed using Databricks and AWS, adhering to the Medallion architecture to structure and refine the data across multiple stages. Specifically, Delta tables were utilized to manage the data within each layer of the architecture, ensuring reliability, consistency, and efficient processing across the Bronze, Silver, and Gold stages.

**1. Data Ingestion and Storage (Bronze Layer)**

Initially, the raw event files were downloaded from the GDELT Events webpage using web scraping and uploaded into an AWS S3 bucket. This cloud architecture platform was chosen because of its scalability, easy connection to Databricks and capacity to handle the large amount of data scraped from GDELT. 

In Databricks, the raw data from S3 was ingested into the Bronze table. This table stores all the raw, unprocessed data as-is, providing an immutable source of truth. The Bronze table initally contains all events for one year, ensuring a comprehensive historical archive that can be reprocessed if necessary.

**2. Data Cleaning and Transformation (Silver Layer)**

The Silver table focuses on data cleaning and refinement. At this stage, the data from the Bronze table was aggregated by URL and by day, ultimately removing duplicate entries to ensure that each news is uniquely represented. In the process of removing duplicates aggregate measures were also computed for each entry, as duplicate URLs did not always have the same values for all columns. Specifically, the Silver table contains the following columns: Average NumSources, Average Tone, Average Goldstein Scale and Average Num Articles. These aggregated metrics provide a more concise and consistent dataset, facilitating more accurate analysis and interpretation in the subsequent stages of the data pipeline

**3. Data Enrichment and Analysis (Gold Layer)**

In the Gold layer the focus is on deriving actionable insights. An importance metric was computed for each news event, weighing each of the factors defined by the columns in the Silver table. This metric helps rank or prioritize events based on their perceived significance.

The Gold table contains the most refined and valuable data, enriched with calculated metrics, and is ready for direct consumption in analytics, reporting, or machine learning models. 

**4. Automated Data Ingestion and Processing**

To ensure the dataset remains current, an automated job was implemented on Databricks to scrape the GDELT Events webpage daily. This job retrieves the latest raw events file, uploads it into the AWS S3 Bucket and passes the new data through the entire data pipeline. In the Bronze layer, the raw daily events are stored in their unprocessed form, maintaining the integrity of the data. These raw events are then cleaned and aggregated in the Silver layer, where duplicate entries are removed and aggregate metrics are computed. Finally, in the Gold layer, the importance metric is recalculated for the new events, ensuring that the most significant news is ready for immediate analysis.

The automated job ensures that the deployed web tool on Streamlit Cloud can access the most up-to-date information, providing users with accurate and timely news summaries based on the latest data from GDELT.

### Data Analysis and Machine Learning 




### Project Deployment

For the project deployment, a Streamlit web application was developed and hosted on Streamlit Cloud. This application is seamlessly integrated with the data warehouse hosted on Databricks, enabling real-time access to the processed data. The frontend of the application features an intuitive menu that allows users to select a specific date range and desired category (Economic, Social or Political). Upon selection, the application retrieves and displays the top 10 news stories within the chosen range and category, along with their respective summaries. This deployment ensures that users can interactively explore and analyze the most relevant news events directly from the processed dataset. 

### Future Work 

Future work on the tool could focus on enhancing user experience and expanding its analytical capabilities. One improvement would be the integration of interactive graphics to visually represent data trends, making the analysis more intuitive. Adding a geographical filter would allow users to narrow down news events by region, providing a more tailored experience. Additionally, implementing sentiment analysis and keyword filtering could offer deeper insights into the nature of the news, helping users identify relevant topics quickly. Another crucial enhancement would be the development of a fake news detection feature, which could assess the credibility of news sources and flag potentially misleading information. 

