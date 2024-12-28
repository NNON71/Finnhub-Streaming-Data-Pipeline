from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka import DeserializingConsumer

def load_schema_registry_client(schema_registry_url):
    return SchemaRegistryClient({'url': schema_registry_url})

def load_avro_deserializer(schema_registry_client, schema_str):
    return AvroDeserializer(schema_registry_client, schema_str)

def load_deserializing_consumer(config: dict) :
    return DeserializingConsumer(config)