from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'realtime_numbers'

while True:
    number = random.randint(1, 100)
    producer.send(topic, {'number': number})
    time.sleep(1)
