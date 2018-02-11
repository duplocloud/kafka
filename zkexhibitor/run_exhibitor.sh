#!/usr/bin/bash -ex


mkdir -p /mnt/zkdata1/zklogs/

java -jar exhibitor-1.0-jar-with-dependencies.jar -c s3 --s3config $EXHIBITOR_S3CONFIG --hostname $DUPLO_DOCKER_HOST
