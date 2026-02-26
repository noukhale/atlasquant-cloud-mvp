# 🚀 AtlasQuant – Cloud-Native AI Trading Advisory MVP

AtlasQuant is a cloud-native FinTech MVP built with a scalable microservices architecture.  
It simulates a real-time AI trading advisory platform using event-driven design principles and modern cloud technologies.

---

## 🧠 Project Overview

AtlasQuant demonstrates:

- Event-driven microservices architecture
- Real-time market data ingestion
- AI decision pipeline (decoupled service)
- Redis caching strategy
- PostgreSQL historical persistence
- Docker containerization
- Kubernetes (Minikube) cloud-ready deployment
- TradingView embedded UI
- WebSocket streaming

This project was built to simulate production-grade cloud architecture patterns.

---

## 🏗 Architecture

![Architecture Diagram](architecture/atlasquant-architecture.png)

### Core Components

| Component | Role |
|------------|------|
| FastAPI Backend | REST + WebSocket API |
| Kafka | Real-time event streaming |
| AI Service | Consumes market data & generates decisions |
| Redis | Cache layer + AI decision storage |
| PostgreSQL | Price history persistence |
| Market Ingestor | Simulated crypto real-time data |
| Kubernetes | Cloud-ready orchestration |
| Docker | Containerization |

---

## ⚙ Tech Stack

- Python (FastAPI)
- Apache Kafka
- Redis
- PostgreSQL
- Docker & Docker Compose
- Kubernetes (Minikube)
- TradingView Widget
- WebSockets

---

## 🔄 Event-Driven Design

1. Market Ingestor publishes market events to Kafka.
2. AI Service consumes market data events.
3. AI decisions are stored in Redis.
4. Backend exposes REST & WebSocket endpoints.
5. PostgreSQL stores historical data.

This design ensures service decoupling and scalability.

---

## 🚀 Run Locally (Docker Compose)

```bash
docker-compose up --build
