from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'financial-data',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

client = MongoClient("mongodb://localhost:27017/")
db = client["finance"]
collection = db["stock_prices"]

for message in consumer:
    data = message.value
    collection.insert_one(data)
    print("Inserted to MongoDB:", data)
