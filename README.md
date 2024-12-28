# Finnhub-Streaming-Data-Pipeline
## Overview
This project involves building a real-time data pipeline using the Finnhub API to ingest stock market data via WebSocket. Apache Kafka is used for streaming, and the project is designed to demonstrate the ingestion, processing, and visualization of real-time stock data. The final output is showcased in a dashboard, making it suitable for inclusion in a data engineering portfolio.

## Features
- **Real-Time Data Ingestion:** Connect to the Finnhub API WebSocket to stream live stock data.
- **Data Streaming with Kafka:** Utilize Apache Kafka to manage and distribute real-time data.
- **Data Processing:** Process data with KSQLDB for aggregation and transformations.
- **Dashboard Visualization:** Display key stock market metrics in an interactive dashboard.
- **Integration with Elasticsearch:** Store processed data for analytics and visualizations.

## What This Project Does
1. **Producer:** Streams real-time stock data from the Finnhub API and sends it to Kafka.
2. **KSQLDB:** Processes raw stock data for aggregations and transformations.
3. **Consumer:** Consumes processed data from Kafka and stores it in Elasticsearch.
4. **Visualization:** Displays analytics and monitoring dashboards using Grafana.

## Tools and Technologies Used
- **Data Streaming:** Apache Kafka
- **API Integration:** Finnhub API (WebSocket)
- **Stream Processing:** KSQLDB
- **Data Storage:** Elasticsearch
- **Visualization:** Grafana
- **Containerization:** Docker & Docker Compose
