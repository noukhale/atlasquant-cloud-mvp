import os
import json
import asyncio
import redis
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI(title="AtlasQuant AI Trading")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# ==============================
# HEALTH
# ==============================
@app.get("/health")
def health():
    return {"status": "ok"}

# ==============================
# AI Latest Decision
# ==============================
@app.get("/ai/latest")
def get_latest_ai(symbol: str = "BTCUSDT"):
    data = r.get(f"ai:{symbol}")
    if not data:
        return {"error": "No AI decision available yet"}
    return json.loads(data)

# ==============================
# WebSocket LIVE AI
# ==============================
@app.websocket("/ws/ai/{symbol}")
async def websocket_ai(websocket: WebSocket, symbol: str):
    await websocket.accept()

    while True:
        data = r.get(f"ai:{symbol}")
        if data:
            await websocket.send_text(data)
        await asyncio.sleep(2)

# ==============================
# FRONTEND PAGE
# ==============================
@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AtlasQuant AI Trading</title>
<script src="https://s3.tradingview.com/tv.js"></script>
</head>
<body style="background:#0b0f19;color:white;font-family:Arial">

<h1>AtlasQuant AI Trading</h1>

<select id="symbol">
  <option value="BTCUSDT">BTCUSDT</option>
  <option value="ETHUSDT">ETHUSDT</option>
</select>

<div id="tradingview_chart" style="height:500px;"></div>

<br>
<button onclick="runAI()">🔍 AI Analyze</button>

<div id="analysis">
Decision: -
<br>
Confidence: -
<br>
Strategy: -
</div>

<script>
let currentSymbol = "BTCUSDT";

function loadChart(symbol){
    new TradingView.widget({
        symbol: "BINANCE:" + symbol,
        interval: "15",
        container_id: "tradingview_chart",
        autosize: true,
        theme: "dark"
    });
}

loadChart(currentSymbol);

document.getElementById("symbol").addEventListener("change", function(){
    currentSymbol = this.value;
    document.getElementById("tradingview_chart").innerHTML = "";
    loadChart(currentSymbol);
    connectWebSocket();
});

async function runAI(){
    const response = await fetch("/ai/latest?symbol=" + currentSymbol);
    const data = await response.json();

    if(data.error){
        document.getElementById("analysis").innerHTML =
        "<span style='color:orange'>AI warming up...</span>";
        return;
    }

    updateAnalysis(data);
}

function updateAnalysis(data){
    let color = "orange";
    if(data.decision === "BUY") color = "lime";
    if(data.decision === "SELL") color = "red";

    document.getElementById("analysis").innerHTML =
        "<span style='color:"+color+"'>Decision: "+data.decision+"</span><br>"+
        "Confidence: "+data.confidence+"<br>"+
        "Strategy: "+data.strategy;
}

let socket;

function connectWebSocket(){
    if(socket) socket.close();

    socket = new WebSocket("ws://localhost:8000/ws/ai/" + currentSymbol);

    socket.onmessage = function(event){
        const data = JSON.parse(event.data);
        updateAnalysis(data);
    };

    socket.onerror = function(){
        document.getElementById("analysis").innerHTML =
        "<span style='color:red'>WebSocket error</span>";
    };
}

connectWebSocket();
</script>

</body>
</html>
"""