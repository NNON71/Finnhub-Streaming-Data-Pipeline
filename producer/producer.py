import websocket
import json
import os
import logging
from dotenv import load_dotenv
from utils.functions import *

load_dotenv()

class FinnhubProducer:
    def __init__(self):
        # Kafka configuration
        self.producer_config = {
            'bootstrap.servers': f"{os.getenv('KAFKA_SERVER')}:{os.getenv('KAFKA_PORT')}"
        }
        
        self.schema_registry_client = load_schema_registry_client(os.getenv('SCHEMA_REGISTRY_URL'))

        # Load schema
        with open('schemas/trader.avsc', 'r') as schema_file:
            schema_str = schema_file.read()
        self.serializer = load_avro_serializer(self.schema_registry_client, schema_str)

        self.producer = load_serializing_producer(self.producer_config, self.serializer)

        # WebSocket setup
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            f"wss://ws.finnhub.io?token={os.getenv('FINNHUB_API_KEY')}",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, ws, message):
        try:
            message = json.loads(message)

            self.producer.produce(
                topic=os.getenv('KAFKA_TOPIC'),
                value=message
            )
            self.producer.flush()
            logging.info(f"Message sent to Kafka: {message}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")

    def on_close(self, ws):
        logging.info("WebSocket closed")

    def on_open(self, ws):
        ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

if __name__ == "__main__":
    FinnhubProducer()