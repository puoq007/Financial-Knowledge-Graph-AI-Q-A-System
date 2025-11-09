# consumer_etl.py
from kafka import KafkaConsumer
from pymongo import MongoClient
import json, time, os
consumer = KafkaConsumer('financial-data',
                         bootstrap_servers=['localhost:29092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         auto_offset_reset='earliest',
                         enable_auto_commit=True)
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo['finance']
col = db['stock_prices']

for msg in consumer:
    data = msg.value
    data['ingested_at'] = time.time()
    col.insert_one(data)
    print("Inserted to Mongo:", data)
