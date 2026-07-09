from pyspark.sql import SparkSession
from pyspark.sql.functions import upper, col, round

spark = SparkSession.builder.appName("SalesTransform").getOrCreate()

input_path = "/mnt/c/Users/ASUS/DBDA Python/airflow/airflow_project/data/sales.csv"
output_path = "/mnt/c/Users/ASUS/DBDA Python/airflow/airflow_project/output/spark_sales_processed"

df = spark.read.csv(input_path, header=True, inferSchema=True)

df = df.withColumn("Sales_Rep", upper(col("Sales_Rep"))) \
    .withColumn("Region", upper(col("Region"))) \
    .withColumn( "Profit_Per_Unit", round(col("Unit_Price") - col("Unit_Cost"), 2) ) \
    .withColumn( "Total_Profit", round( (col("Unit_Price") - col("Unit_Cost")) * col("Quantity_Sold"),
            2
        )
    )

df.write.mode("overwrite").option("header", True).csv(output_path)

print("Spark transformation completed")

spark.stop()