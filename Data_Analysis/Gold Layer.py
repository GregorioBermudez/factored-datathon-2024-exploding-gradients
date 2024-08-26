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


# COMMAND ----------

# Verify transformation
print(f"Row count in {gold_table_name}:")
spark.sql(f"SELECT COUNT(*) FROM {gold_table_name}").show()

# COMMAND ----------

# Display sample data
print(f"Sample data from {gold_table_name}:")
spark.sql(f"SELECT * FROM {gold_table_name} LIMIT 5").show()

