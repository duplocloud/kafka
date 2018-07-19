import requests
import pprint
from os import environ
from os import system
import json
import time
import sys
from logger import logging

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('zookeeper-launch')
logger.setLevel(logging.DEBUG)
pp = pprint.PrettyPrinter(indent=4)

discovery_ep = environ.get('DISCOVERY_EP') + '/subscriptions/' + environ.get('TENANT_ID')
logger.info("Discovery endpoint %s", discovery_ep)

headers = json.loads('{"Content-type": "application/json"}')
getUrl = discovery_ep + '/getpods'
response = requests.get(getUrl, headers=headers)
response.raise_for_status()
#pp.pprint(response.json())

role_name = environ.get('ROLE_NAME')
logger.info("Role %s", role_name)

lExpectedHosts = {}
for pod in response.json():
    if pod["DesiredStatus"] != 1:
        continue
    if pod["Name"] != role_name:
        continue	
	
    lExpectedHosts[str(pod["Host"])] = str(pod["Host"])
    logger.info('Added ZK Host %s to lExpectedHosts', pod["Host"])
	
getUrl = discovery_ep + '/getMinions'
response = requests.get(getUrl, headers=headers)
response.raise_for_status()
#pp.pprint(response.json())

#del environ["ZOOKEEPER_SERVERS"]		
list = None		
for host in response.json():
    if host["Name"] in lExpectedHosts:
        if list is None:
            list = host["DirectAddress"] + ":22888:23888"
        else:
            list = list + ";" + host["DirectAddress"] + ":22888:23888"

print list

cmd = 'export ZOOKEEPER_SERVERS="' + list + '"'
with open('ex.sh', 'w') as the_file:
    the_file.write(cmd)


