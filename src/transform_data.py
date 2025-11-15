from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os

spark = SparkSession.builder.appName('LoadCSV').getOrCreate()

data_path = os.path.expanduser('~/end-to-end-sensor-api/data/raw/')
files_list = [f for f in os.listdir(data_path) if f.endswith('.csv')]

all_data = None
for file in files_list:
    file_path = os.path.join(data_path, file)
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    if all_data is None:
        all_data = df
    else:
        all_data = all_data.union(df)
all_data.show(5)


data_by_day = (all_data
                  .groupBy('date','id_magasin')
                  .agg(F.round(F.sum('nombre_visiteurs'),2).alias('total_visiteurs'))
                  .orderBy('date'))

data_by_day.show()
