from datasets import load_dataset
from pyspark.sql import SparkSession
import pandas as pd
import re

ds = load_dataset("BI55/MedText", split="train")
spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame(ds.to_pandas())

def getAges():
    ages = []

    rows = df.collect()  # bring all rows into Python
    for row in rows:
        text = row["Prompt"]
        numbers = re.findall(r'\b\d+\b', text)

        if numbers != []:
            number = numbers[0]
            ages.append(number)

    return ages