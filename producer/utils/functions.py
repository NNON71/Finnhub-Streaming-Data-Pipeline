from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

def load_schema_registry_client(schema_registry_url):
    return SchemaRegistryClient({'url': schema_registry_url})

def load_avro_serializer(schema_registry_client, schema_str):
    return AvroSerializer(schema_registry_client, schema_str)

def load_serializing_producer(config: dict, value_serializer):
    config.update({
        'value.serializer': value_serializer
    })
    return SerializingProducer(config)