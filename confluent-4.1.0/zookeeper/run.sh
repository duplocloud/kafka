#!/bin/bash

python /launch-zk.py
source ex.sh
export ZOOKEEPER_SERVER_ID=$REPLICA_ID
export ZOOKEEPER_CLIENT_PORT=22181
export ZOOKEEPER_TICK_TIME=2000
export ZOOKEEPER_INIT_LIMIT=5
export ZOOKEEPER_SYNC_LIMIT=2
echo $ZOOKEEPER_SERVERS
/etc/confluent/docker/run
