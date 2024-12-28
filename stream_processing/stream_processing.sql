-- สร้าง stream สำหรับการจัดการข้อมูลดิบจาก Kafka topic
CREATE STREAM stock_stream (
    data ARRAY<STRUCT<
        c ARRAY<STRING>,  
        p DOUBLE,          
        s STRING,          
        t BIGINT,          
        v DOUBLE          
    >>,
    type STRING           
) WITH (
    KAFKA_TOPIC = 'stock_prices',
    VALUE_FORMAT = 'AVRO'
);

-- สร้าง stream ใหม่ที่แปลงข้อมูลให้แบนราบ (Flattened)
CREATE STREAM flat_stock_stream AS
SELECT
    data[1]->c AS currencies_1,
    data[1]->p AS price_1,
    data[1]->s AS symbol_1,
    data[1]->t AS trade_time_1,
    data[1]->v AS volume_1
FROM stock_stream
EMIT CHANGES;

-- ตรวจสอบข้อมูลเพิ่มเติม เช่น ราคาเฉลี่ยของข้อมูลใน stream (optional)
CREATE TABLE avg_price_table AS
SELECT
    symbol_1 AS symbol,
    AVG(price_1) AS avg_price_1
FROM flat_stock_stream
GROUP BY symbol_1
EMIT CHANGES;
