from elasticsearch import Elasticsearch
from datetime import datetime
from dotenv import load_dotenv
from utils.functions import *
import os
import logging
from confluent_kafka import KafkaError

load_dotenv()

# ตั้งค่า Elasticsearch
es = Elasticsearch(hosts=["http://elasticsearch:9200/"])

def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).isoformat() + "Z"

# ฟังก์ชันบันทึกข้อมูลแบบ Bulk
buffer = []

def save_bulk_to_elasticsearch(index, docs):
    from elasticsearch.helpers import bulk
    try:
        if docs:
            bulk(es, docs, index=index)
            logging.info(f"Saved {len(docs)} documents to Elasticsearch.")
    except Exception as e:
        logging.error(f"Failed to save documents to Elasticsearch: {e}")

# โหลด Schema Registry และ Deserializer
schema_registry_client = load_schema_registry_client(os.getenv('SCHEMA_REGISTRY_URL'))

with open('schemas/trader.avsc', 'r') as schema_file:
    schema_str = schema_file.read()

deserializer = load_avro_deserializer(schema_registry_client, schema_str)

# ตั้งค่า DeserializingConsumer
consumer_config = {
    'bootstrap.servers': f"{os.getenv('KAFKA_SERVER')}:{os.getenv('KAFKA_PORT')}",
    'group.id': 'kafka-elasticsearch-consumer',
    'auto.offset.reset': 'earliest',
    'value.deserializer': deserializer  # ใช้ AvroDeserializer
}

consumer = load_deserializing_consumer(consumer_config)
consumer.subscribe([os.getenv('KAFKA_TOPIC')])

logging.info(f"Connecting to Kafka at {os.getenv('KAFKA_SERVER')}:{os.getenv('KAFKA_PORT')}")
logging.info(f"Subscribed to Kafka topic: {os.getenv('KAFKA_TOPIC')}")
logging.info(f"Connecting to Elasticsearch at http://elasticsearch:9200/")

try:
    while True:
        msg = consumer.poll(0.1)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.warning(f"End of partition reached {msg.topic()}-{msg.partition()} at offset {msg.offset()}")
            else:
                logging.error(f"Consumer error: {msg.error()}")
            continue

        # ดึงค่าที่ถูก deserialize แล้ว
        try:
            record_value = msg.value()
            logging.info(f"Processing record: {record_value}")

            if "data" in record_value and isinstance(record_value["data"], list):
                record_value["@timestamp"] = format_timestamp(record_value["data"][0]["t"])
                buffer.append({"_source": record_value})
            
            if len(buffer) >= 100:
                save_bulk_to_elasticsearch('trader-data', buffer)
                buffer.clear()
        except Exception as e:
            logging.error(f"Failed to process message: {e}")

        # บันทึก buffer ที่เหลือในแต่ละ loop
        if len(buffer) > 0:
            save_bulk_to_elasticsearch('trader-data', buffer)
            buffer.clear()

except KeyboardInterrupt:
    logging.info("Shutting down consumer...")
    save_bulk_to_elasticsearch('trader-data', buffer)  # บันทึกข้อมูลที่เหลืออยู่ใน buffer
finally:
    consumer.close()
