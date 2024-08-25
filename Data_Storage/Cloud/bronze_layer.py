# Databricks notebook source
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# Define the schema
schema = StructType([
    StructField("GlobalEventID", IntegerType(), False),
    StructField("Day", IntegerType(), False),
    StructField("MonthYear", IntegerType(), False),
    StructField("Year", IntegerType(), False),
    StructField("FractionDate", DoubleType(), False),
    StructField("Actor1Code", StringType(), True),
    StructField("Actor1Name", StringType(), True),
    StructField("Actor1CountryCode", StringType(), True),
    StructField("Actor1KnownGroupCode", StringType(), True),
    StructField("Actor1EthnicCode", StringType(), True),
    StructField("Actor1Religion1Code", StringType(), True),
    StructField("Actor1Religion2Code", StringType(), True),
    StructField("Actor1Type1Code", StringType(), True),
    StructField("Actor1Type2Code", StringType(), True),
    StructField("Actor1Type3Code", StringType(), True),
    StructField("Actor2Code", StringType(), True),
    StructField("Actor2Name", StringType(), True),
    StructField("Actor2CountryCode", StringType(), True),
    StructField("Actor2KnownGroupCode", StringType(), True),
    StructField("Actor2EthnicCode", StringType(), True),
    StructField("Actor2Religion1Code", StringType(), True),
    StructField("Actor2Religion2Code", StringType(), True),
    StructField("Actor2Type1Code", StringType(), True),
    StructField("Actor2Type2Code", StringType(), True),
    StructField("Actor2Type3Code", StringType(), True),
    StructField("IsRootEvent", IntegerType(), True),
    StructField("EventCode", StringType(), True),
    StructField("EventBaseCode", StringType(), True),
    StructField("EventRootCode", StringType(), True),
    StructField("QuadClass", IntegerType(), True),
    StructField("GoldsteinScale", DoubleType(), True),
    StructField("NumMentions", IntegerType(), True),
    StructField("NumSources", IntegerType(), True),
    StructField("NumArticles", IntegerType(), True),
    StructField("AvgTone", DoubleType(), True),
    StructField("Actor1Geo_Type", IntegerType(), True),
    StructField("Actor1Geo_Fullname", StringType(), True),
    StructField("Actor1Geo_CountryCode", StringType(), True),
    StructField("Actor1Geo_ADM1Code", StringType(), True),
    StructField("Actor1Geo_Lat", DoubleType(), True),
    StructField("Actor1Geo_Long", DoubleType(), True),
    StructField("Actor1Geo_FeatureID", StringType(), True),
    StructField("Actor2Geo_Type", IntegerType(), True),
    StructField("Actor2Geo_Fullname", StringType(), True),
    StructField("Actor2Geo_CountryCode", StringType(), True),
    StructField("Actor2Geo_ADM1Code", StringType(), True),
    StructField("Actor2Geo_Lat", DoubleType(), True),
    StructField("Actor2Geo_Long", DoubleType(), True),
    StructField("Actor2Geo_FeatureID", StringType(), True),
    StructField("ActionGeo_Type", IntegerType(), True),
    StructField("ActionGeo_Fullname", StringType(), True),
    StructField("ActionGeo_CountryCode", StringType(), True),
    StructField("ActionGeo_ADM1Code", StringType(), True),
    StructField("ActionGeo_Lat", DoubleType(), True),
    StructField("ActionGeo_Long", DoubleType(), True),
    StructField("ActionGeo_FeatureID", StringType(), True),
    StructField("DATEADDED", IntegerType(), False),
    StructField("SOURCEURL", StringType(), False)
])

# Create a Spark session
spark = SparkSession.builder.appName("BronzeLayerIngestion").getOrCreate()

# Configuration
bronze_bucket = "datathonfactored2024"
folder_path = f"s3://datathonfactored2024/GDELT Event Files/"  # Ruta a la carpeta

# Read all CSV files from the specified S3 folder with the defined schema
df = spark.read.format("csv") \
    .option("header", "false") \
    .option("delimiter", "\t") \
    .schema(schema) \
    .load(folder_path)  # Carga todos los archivos en la carpeta

# Add metadata columns
df_with_metadata = df.withColumn("ingestion_timestamp", current_timestamp())

# Write to Delta table
df_with_metadata.write.format("delta") \
    .mode("append") \
    .saveAsTable("bronze_layer")

print(f"Data ingested into Bronze layer table from folder: {folder_path}")

# Optional: Display the first few rows of the ingested data
df_with_metadata.show(5)

