import os
import json
import time
import random
import redis

r = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=6379, decode_responses=True)

symbols = ["BTCUSDT","ETHUSDT"]

while True:
    for symbol in symbols:
        decision = random.choice(["BUY","SELL","HOLD"])
        confidence = round(random.uniform(0.6,0.95),2)

        data = {
            "symbol": symbol,
            "decision": decision,
            "confidence": confidence,
            "strategy": "RSI_AI_v1",
            "timestamp": int(time.time())
        }

        r.set(f"ai:{symbol}", json.dumps(data))

    time.sleep(3)