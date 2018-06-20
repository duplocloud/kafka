#!/bin/bash -e

sleep 20s
cd /opt/kafka_2.11-1.0.0
sed -i 's/DUPLO_DOCKER_HOST/'"$DUPLO_DOCKER_HOST"'/' config/server.properties
sed -i 's/ROLE_DNS_NAME/'"$ROLE_DNS_NAME"'/' config/server.properties

./bin/kafka-server-start.sh config/server.properties