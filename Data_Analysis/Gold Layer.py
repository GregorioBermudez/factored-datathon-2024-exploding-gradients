# Databricks notebook source
# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, abs, max, lit, datediff, to_date
from pyspark.sql.window import Window
import pyspark.sql.functions as F

# COMMAND ----------

# Initialize Spark Session
spark = SparkSession.builder.appName("GoldLayerTransformation").getOrCreate()

# COMMAND ----------

# Configuration
silver_table_name = "silver_layer"
gold_table_name = "gold_layer"

# COMMAND ----------

def calculate_importance(df):
    """
    Calculates the importance score for each row in the dataframe.
    """
    window = Window.partitionBy()
    max_num_sources = df.select(max("AvgNumSources")).first()[0]
    max_abs_tone = df.select(max(abs("AvgAvgTone"))).first()[0]
    
    return df.withColumn(
        "Importance",
        (2 * col("AvgNumSources") / lit(max_num_sources)) + 
        (abs(col("AvgAvgTone")) / lit(max_abs_tone))
    )

# COMMAND ----------

# def get_sorted_data(df, num_urls):
#     """
#     Sorts the given data based on the importance score and returns the top 'num_urls' rows.
#     """
#     return df.orderBy(col("Importance").desc()).limit(num_urls)

# COMMAND ----------

# def get_urls(start_date, end_date, num_urls):
#     """
#     Retrieves a list of URLs based on the given start date, end date, and number of URLs.
#     """
#     # Read from Silver table
#     df = spark.table(silver_table_name)
    
#     # Filter by date range
#     df_filtered = df.filter(
#         (col("Day") >= start_date) & 
#         (col("Day") <= end_date)
#     )
    
#     # Calculate importance
#     df_with_importance = calculate_importance(df_filtered)
    
#     # Get top URLs
#     top_urls = get_sorted_data(df_with_importance, num_urls)
    
#     return top_urls

# COMMAND ----------

def transform_to_gold():
    """
    Transforms all data from Silver to Gold layer, adding the Importance score.
    """
    # Read from Silver table
    silver_df = spark.table(silver_table_name)
    
    # Calculate importance for all rows
    gold_df = calculate_importance(silver_df)
    
    # Write to Gold Delta table
    gold_df.write.format("delta") \
        .mode("overwrite") \
        .saveAsTable(gold_table_name)
    
    print(f"All data transformed and saved to {gold_table_name}")

# COMMAND ----------
transform_to_gold()


# urls = transform_to_gold(start_date, end_date, num_urls)
# print(f"Top {num_urls} URLs:")
# for url in urls:
#     print(url)

# COMMAND ----------

# Verify transformation
print(f"Row count in {gold_table_name}:")
spark.sql(f"SELECT COUNT(*) FROM {gold_table_name}").show()

# COMMAND ----------

# Display sample data
print(f"Sample data from {gold_table_name}:")
spark.sql(f"SELECT * FROM {gold_table_name} LIMIT 5").show()

