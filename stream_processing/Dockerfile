FROM confluentinc/cp-ksqldb-server:7.8.0

COPY ksql-init.sh /usr/local/bin/ksql-init.sh

COPY stream_processing.sql /docker-entrypoint-initdb.d/stream_processing.sql

# RUN /usr/local/bin/ksql-init.sh

# ENTRYPOINT ["/usr/local/bin/ksql-init.sh"]