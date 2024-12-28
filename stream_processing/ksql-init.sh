#!/bin/bash
set -e

# ตรวจสอบว่า ksqldb-server พร้อมใช้งานหรือไม่
echo "Waiting for ksqldb-server to be ready..."

until curl -s http://ksqldb-server:8088/info; do
  echo "ksqldb-server is not ready yet. Retrying in 5 seconds..."
  sleep 5
done

echo "ksqldb-server is ready! Running SQL scripts."

# รัน SQL scripts เมื่อเซิร์ฟเวอร์พร้อมใช้งาน
cat /docker-entrypoint-initdb.d/stream_processing.sql | ksql http://ksqldb-server:8088