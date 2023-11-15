import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql import functions
from pyspark.sql.types import StructType, StructField, BooleanType, IntegerType, FloatType, ArrayType, StringType

# Set Spark configurations
spark_conf = SparkConf() \
    .setAppName("KafkaSparkIntegration") \
    .set("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
    .set("spark.executor.memory", "2g") \
    .set("spark.executor.cores", "2") \
    .set("spark.cores.max", "2") \
    .set("spark.sql.shuffle.partitions", "4")

# Create Spark session
spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

# Define Kafka consumer configuration
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_movies") \
    .option("startingOffsets", "earliest") \
    .load()

# Select the 'value' column and cast it to STRING
value_df = df.selectExpr("CAST(value AS STRING)")

schema = StructType([
    StructField("adult", BooleanType(), True),
    StructField("backdrop_path", StringType(), True),
    StructField("belongs_to_collection", StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("poster_path", StringType(), True),
        StructField("backdrop_path", StringType(), True)
    ]), True),
    StructField("budget", IntegerType(), True),
    StructField("genres", ArrayType(StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])), True),
    StructField("homepage", StringType(), True),
    StructField("id", IntegerType(), True),
    StructField("imdb_id", StringType(), True),
    StructField("original_language", StringType(), True),
    StructField("original_title", StringType(), True),
    StructField("overview", StringType(), True),
    StructField("popularity", FloatType(), True),
    StructField("poster_path", StringType(), True),
    StructField("production_companies", ArrayType(StructType([
        StructField("id", IntegerType(), True),
        StructField("logo_path", StringType(), True),
        StructField("name", StringType(), True),
        StructField("origin_country", StringType(), True)
    ])), True),
    StructField("production_countries", ArrayType(StructType([
        StructField("iso_3166_1", StringType(), True),
        StructField("name", StringType(), True)
    ])), True),
    StructField("release_date", StringType(), True),
    StructField("revenue", IntegerType(), True),
    StructField("runtime", IntegerType(), True),
    StructField("spoken_languages", ArrayType(StructType([
        StructField("english_name", StringType(), True),
        StructField("iso_639_1", StringType(), True),
        StructField("name", StringType(), True)
    ])), True),
    StructField("status", StringType(), True),
    StructField("tagline", StringType(), True),
    StructField("title", StringType(), True),
    StructField("video", BooleanType(), True),
    StructField("vote_average", FloatType(), True),
    StructField("vote_count", IntegerType(), True)
])
# Apply the schema to parse JSON data
selected_df = value_df.withColumn("values", functions.from_json(value_df["value"], schema)).selectExpr("values")

# Select specific columns for further processing
result_df = selected_df.select(
    functions.col("values.adult").alias("adult"),
    functions.col("values.belongs_to_collection").alias("belongs_to_collection"),
    functions.col("values.belongs_to_collection.name").alias("name_collection"),
    functions.col("values.budget").alias("budget"),
    functions.col("values.genres.id").alias("id"),
    functions.col("values.genres.name").alias("genres_name"),
    functions.col("values.original_language").alias("original_language"),
    functions.col("values.overview").alias("overview"),
    functions.col("values.popularity").alias("popularity"), 
    functions.col("values.production_companies.name").alias("name_production_company"),
    functions.col("values.status").alias("status"),
    functions.col("values.production_companies.id").alias("id_production_company"),   
    functions.col("values.production_companies.origin_country").alias("origin_country_production_company"),
    functions.col("values.production_countries.name").alias("name_production_countries"),  
    functions.col("values.release_date").alias("release_date"),
    functions.col("values.revenue").alias("revenue"),
    functions.col("values.tagline").alias("tagline"),
    functions.col("values.title").alias("title"),
    functions.col("values.video").alias("video"),
    functions.col("values.vote_average").alias("vote_average"),
    functions.col("values.vote_count").alias("vote_count"),
)

# Define additional transformations/enrichments here
result_df = result_df.withColumn("description", functions.concat_ws(" ", "title", "overview"))

# Normalize popularity and vote_average fields
result_df = result_df.withColumn("popularity", functions.round("popularity", 2))
result_df = result_df.withColumn("vote_average", functions.round("vote_average", 2))

query = result_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("append") \
    .option("es.resource", "user_movies") \
    .option("es.nodes", "localhost") \
    .option("es.port", "9200") \
    .option("es.nodes.wan.only", "false")\
    .option("es.index.auto.create", "true")\
    .option("checkpointLocation", "./checkpointLocation/") \
    .start()

query = result_df.writeStream.outputMode("append").format("console").start()

query.awaitTermination()
