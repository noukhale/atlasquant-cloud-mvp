import asyncio
import json
import websockets
from kafka import KafkaProducer
import os

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BROKER"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

async def stream():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            price = float(data["p"])

            event = {
                "symbol": "BTCUSDT",
                "price": price
            }

            producer.send("market-events", event)
            producer.flush()

            print("BTC:", price)

asyncio.run(stream())