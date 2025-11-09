# producer.py
from kafka import KafkaProducer
import json, time, random
producer = KafkaProducer(bootstrap_servers=['localhost:29092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

companies = ["Tesla","Apple","Google","Microsoft"]
while True:
    msg = {"company": random.choice(companies),
           "price": round(random.uniform(100, 1500),2),
           "ts": time.time()}
    producer.send("financial-data", value=msg)
    producer.flush()
    print("Sent:", msg)
    time.sleep(2)
