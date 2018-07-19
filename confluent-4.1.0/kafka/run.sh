#!/bin/bash

python /launch-kafka.py
source ex.sh
echo $KAFKA_ZOOKEEPER_CONNECT
echo $KAFKA_ADVERTISED_LISTENERS
/etc/confluent/docker/run
