# Databricks notebook source
# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, current_timestamp

# COMMAND ----------

# Initialize Spark Session
spark = SparkSession.builder.appName("SilverLayerTransformation").getOrCreate()

# COMMAND ----------

# Configuration
bronze_table_name = "bronze_layer"
silver_table_name = "silver_layer"

# COMMAND ----------

def clean_dataframe(df):
    """
    Cleans the given dataframe by performing the following operations:
    1. Group the dataframe by 'source_url' and 'dateadded' columns.
    2. Calculate the mean of the following columns: 'num_sources', 'avg_tone', 'goldstein_scale', 'num_articles'.
    3. Return the cleaned dataframe.
    
    Parameters:
    - df: pyspark.sql.DataFrame
      The input dataframe to be cleaned.
    
    Returns:
    - pyspark.sql.DataFrame
      The cleaned dataframe.
    """
    clean_data = df.groupBy('SOURCEURL', 'Day').agg(
        mean('NumSources').alias('AvgNumSources'),
        mean('AvgTone').alias('AvgAvgTone'),
        mean('GoldsteinScale').alias('AvgGoldsteinScale'),
        mean('NumArticles').alias('AvgNumArticles')
    )
    
    # Add a timestamp for when this transformation was performed
    clean_data = clean_data.withColumn("transform_timestamp", current_timestamp())
    
    return clean_data

def transform_to_silver():
    # Read from Bronze table
    bronze_df = spark.table(bronze_table_name)
    
    # Apply cleaning transformation
    silver_df = clean_dataframe(bronze_df)
    
    # Write to Silver Delta table
    silver_df.write.format("delta") \
        .option("mergeSchema", "true") \
        .mode("overwrite") \
        .saveAsTable(silver_table_name)
    
    print(f"Data transformed and saved to {silver_table_name}")

# Execute the transformation
transform_to_silver()

# Verify transformation
print(f"Row count in {silver_table_name}:")
spark.sql(f"SELECT COUNT(*) FROM {silver_table_name}").show()

# Display sample data
print(f"Sample data from {silver_table_name}:")
spark.sql(f"SELECT * FROM {silver_table_name} LIMIT 5").show()
