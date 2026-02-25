import json
import os
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BROKER", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_market_event(data):
    producer.send("market-events", data)
    producer.flush()
