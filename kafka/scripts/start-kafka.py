#!/usr/bin/env python

import os
import subprocess
import sys
import ConfigParser

KAFKA_HOME = '/kafka'
DATA_DIR= '/mnt/kafkadata1/kafka-logs'

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
DUPLO_DOCKER_HOST = os.environ['DUPLO_DOCKER_HOST']
ROLE_NAME = os.environ['ROLE_NAME']
BROKER_ID = int(ROLE_NAME.replace('kafka-', ''))
HOST_SUFFIX = os.environ['HOST_SUFFIX']
ZOOKEEPER_HOSTS = os.environ['ZOOKEEPER_HOSTS']


HEAP_OPTS = '-Xmx1G -Xms1G'
ZK_CHROOT = '/kafka'
ZOOKEEPER_CONNECT = ZOOKEEPER_HOSTS + ZK_CHROOT

COMMON_OVERRIDES = [
	('controlled.shutdown.enable', 'true'),
	('auto.create.topics.enable', 'false'),
	('log.dirs', DATA_DIR)
]


class KafkaRun(object):
	def __init__(self, kafka_home):
		self.kafka_home = kafka_home
		self.args = []

	def override(self, key, val):
		self.args.append('--override {}={}'.format(key, val))
		return self

	def run(self):
		os.environ['KAFKA_HEAP_OPTS'] = HEAP_OPTS
		command_name = '{0}/bin/kafka-server-start.sh {0}/config/server.properties'.format(self.kafka_home)
		full_command = '{} {}'.format(command_name, ' '.join(self.args))
		print 'Running {}'.format(full_command)
		sys.exit(subprocess.call(full_command, shell=True))


def main():
	kafka = KafkaRun(
		KAFKA_HOME
	).override(
		'zookeeper.connect', ZOOKEEPER_CONNECT
	).override(
		'broker.id', BROKER_ID
	).override(
		'listeners', 'PLAINTEXT://{}:9092'.format(DUPLO_DOCKER_HOST)
	).override(
		'advertised.listeners', 'PLAINTEXT://{}{}:9092'.format(ROLE_NAME, HOST_SUFFIX)
	)
	for key, value in COMMON_OVERRIDES:
		kafka.override(key, value)
	kafka.run()


if __name__ == '__main__':
	main()
