"""
 Consumes messages from one or more topics in Kafka and does an equation.
 Usage: spark_equation.py <bootstrap-servers> <subscribe-type> <topics>
   <bootstrap-servers> The Kafka "bootstrap.servers" configuration. A
   comma-separated list of host:port.
   <subscribe-type> There are three kinds of type, i.e. 'assign', 'subscribe',
   'subscribePattern'.
   |- <assign> Specific TopicPartitions to consume. Json string
   |  {"topicA":[0,1],"topicB":[2,4]}.
   |- <subscribe> The topic list to subscribe. A comma-separated list of
   |  topics.
   |- <subscribePattern> The pattern used to subscribe to topic(s).
   |  Java regex string.
   |- Only one of "assign, "subscribe" or "subscribePattern" options can be
   |  specified for Kafka source.
   <topics> Different value format depends on the value of 'subscribe-type'.

 Run the example
    `$ bin/spark-submit examples/src/main/python/sql/streaming/spark_equation.py \
    host1:port1,host2:port2 subscribe topic1,topic2`
    
    bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3 /home/rsi-psd-vm/Documents/rsi-psd-codes/psd/2019-2/SEILA/spark_equation.py localhost:9092 subscribe fila

"""
from __future__ import print_function

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import from_json
from pyspark.sql.types import *

from rsiarthur import celsius_to_fahrenheit, heat_index_fahrenheit_alg

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        Usage: spark_equation.py <bootstrap-servers> <subscribe-type> <topics>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]

    spark = SparkSession\
        .builder\
        .appName("SparkEquation")\
        .getOrCreate()

    
    df = spark.readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("subscribe", "fila")\
        .option("startingOffsets", "latest")\
        .load()
    
    personJsonDf = df.selectExpr("CAST(value AS STRING)")

    # ola = personJsonDf.foreach(printEach)

    struct = StructType([
        StructField("umidade_maxima", StringType(), True),
        StructField("temperatura_maxima", StringType(), True),
        StructField("temperatura_minima", StringType(), True),
        StructField("umidade_minima", StringType(), True)
    ])

    personNestedDf = personJsonDf.select(from_json("value", struct).alias("values"))

    # personNestedDf.printSchema()
    
    personFlattenedDf = personNestedDf.selectExpr("values.temperatura_maxima", "values.temperatura_minima", "values.umidade_maxima", "values.umidade_minima")

    def printEach(x):
        # print(indiceDeCalor(float(x[0]), float(x[2])))
        # print(x[0], x[1], x[2], x[3])
        print(heat_index_fahrenheit_alg(celsius_to_fahrenheit(float(x[0])), float(x[2])))

    consoleOutput = personFlattenedDf\
        .writeStream\
        .foreach(printEach)\
        .start()
        # .outputMode("append")\
        # .format("console")\
    # consoleOutput.awaitTermination()