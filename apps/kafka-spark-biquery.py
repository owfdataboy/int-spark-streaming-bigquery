from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# Init spark session
spark = SparkSession \
  .builder \
  .appName('spark-bigquery') \
  .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.23.2.jar") \
  .getOrCreate()

# GCS temporary bucket
bucket = "dataproc-test-to-bigquery"
spark.conf.set('temporaryGcsBucket', bucket)

# Read message from kafka consumer
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "34.121.179.78:9092") \
  .option("subscribe", "test-topic") \
  .load()

# Convert binary to string
df_to_string = df.withColumn('value_string', df.value.cast('string'))

# Saving the data to BigQuery
query = df_to_string.writeStream.format('bigquery') \
  .option("project", "int-ml-ai") \
  .option('table', 'streaming_kafka.test_streaming') \
  .option("checkpointLocation", "/tmp/spark/checkpoint") \
  .start()

# Wait to exception to stop the job
query.awaitTermination()