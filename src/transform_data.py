from pyspark.sql import SparkSession
import os

spark = SparkSession.builder.appName('LoadCSV').getOrCreate()

data_path = os.path.expanduser('~/end-to-end-sensor-api/data/raw/')
files_list = [f for f in os.listdir(data_path) if f.endswith('.csv')]
dataframes = {}

for i, file in enumerate(files_list):
    file_path = os.path.join(data_path, file)
    dataframes[i] = spark.read.csv(file_path, header=True, inferSchema=True)
    print(f"Dataframe {i}: {file}")
    dataframes[i].show()