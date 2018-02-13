Zookeepeer Installation Steps

1. EC2 Instance Setup
	a. Create a t2.large instance with 
		- Host volume mappings as [{"Name": "/dev/xvdf", "VolumeType": "io1", "Size": "100", "Iops": "1000"}]
		- Allocation tag as zk-exhibitor-1
		- userdata: IyEgL2Jpbi9iYXNoDQpzdWRvIG1rZnMgLXQgZXh0NCAvZGV2L3h2ZGYNCnN1ZG8gbWtkaXIgL21udC96a2RhdGExDQpzdWRvIGVjaG8gIm1vdW50IC9kZXYveHZkZiAvbW50L3prZGF0YTEiID4gL2V0Yy9yYy5sb2NhbA0Kc3VkbyBlY2hvICJleGl0IDAiID4+IC9ldGMvcmMubG9jYWwNCnN1ZG8gcmVib290DQo=
        The above userdata is base64 version of the following script:
        #! /bin/bash
		sudo mkfs -t ext4 /dev/xvdf
		sudo mkdir /mnt/zkdata1
		sudo echo "mount /dev/xvdf /mnt/zkdata1" > /etc/rc.local
		sudo echo "exit 0" >> /etc/rc.local
		sudo reboot

2. S3 setup
   a. Create an S3 bucket called zookeeper and a folder inside it called configs
   b. In the file zookeeper/exhibitor-s3.conf replace the 10.77.x.x IP address of the EC2 instance IP above and upload the file into the above s3 folder

3. Microservice setup
   a. Service Setup:
   	- Name: zk-exhibitor-1
   	- Image: duplocloud/kafka:zkexhibitor_v0
   	- Env: { "EXHIBITOR_S3CONFIG": "duploservices-kafka-zookeeper:configs/exhibitor-s3.conf", "HOSTNAME_SUFFIX": "<domain_suffix>" } where domainsuffix is the part of the dns name after zk-exhibitor-1 (for example -kafka.duplopoc.net assuming kafka is the name of the duplo tenant)
   	- Allocation tag: zk-exhibitor-1
   	- Volume Mount: "/mnt/zkdata1:/mnt/zkdata1"
   	- Docker Host config: {"NetworkMode": "host", "CapAdd": [ "NET_ADMIN" ]}

   b. ELB setup: 
   	a. External and LB port 2181. native App mode instead of Docker Mode. Note down the DNS name which will be used in Kafka setup next
   	b. External port 80 and LB port 8080. native App mode instead of Docker Mode

Kafka Installation Steps

1. EC2 Instance Setup
	a. Create a m4.large instance with 
		- Host volume mappings as [{"Name": "/dev/xvdf", "VolumeType": "st1", "Size": "500", "Iops": null}]
		- Allocation tag as kafka-101
		- userdata: IyEgL2Jpbi9iYXNoDQpzdWRvIGVjaG8gIm1rZGlyIC1wIC9tbnQva2Fma2FkYXRhMSIgPiAvZXRjL3JjLmxvY2FsDQpzdWRvIGVjaG8gIm1vdW50IC9kZXYveHZkZiAvbW50L2thZmthZGF0YTEgLW8gbm9hdGltZSIgPj4gL2V0Yy9yYy5sb2NhbA0Kc3VkbyBlY2hvICJzeXNjdGwgdm0uc3dhcHBpbmVzcz0xIiA+PiAvZXRjL3JjLmxvY2FsDQpzdWRvIGVjaG8gInN5c2N0bCB2bS5kaXJ0eV9iYWNrZ3JvdW5kX3JhdGlvPTUiID4+IC9ldGMvcmMubG9jYWwNCnN1ZG8gZWNobyAic3lzY3RsIHZtLmRpcnR5X3JhdGlvPTYwIiA+PiAvZXRjL3JjLmxvY2FsDQpzdWRvIHJlYm9vdA==
		The above userdata is the base64 version of the following script:
		#! /bin/bash
		sudo echo "mkdir -p /mnt/kafkadata1" > /etc/rc.local
		sudo echo "mount /dev/xvdf /mnt/kafkadata1 -o noatime" >> /etc/rc.local
		sudo echo "sysctl vm.swappiness=1" >> /etc/rc.local
		sudo echo "sysctl vm.dirty_background_ratio=5" >> /etc/rc.local
		sudo echo "sysctl vm.dirty_ratio=60" >> /etc/rc.local
		sudo reboot

3. Microservice setup
   a. Service Setup:
   	- Name: kafka-101
   	- Image: duplocloud/kafka:kafka_v2
   	- Env: { "JMX_PORT": 9999, "ZOOKEEPER_HOSTS":"<dnsname>:2181", "HOST_SUFFIX":".<dnsdomain>" } where dns name is shown in the column called dns in the services tab next to the service zk-exhibitor-1 (for example zk-exhibitor-1-kafka.duplopoc.net) where domainsuffix is the part of the dns name after zk-exhibitor-1 (for example -kafka.duplopoc.net assuming kafka is the name of the duplo tenant). Basically domainsuffix is part of the dns name that is constant for all services within the tenant. Typically it is "-<tenantname>.<domainoftheorg>" where domainoftheorg is constant per duplo deployment.
   	- Allocation tag: kafka-101
   	- Volume Mount: "/mnt/kafkadata1:/mnt/kafkadata1"
   	- Docker Host config: {"NetworkMode": "host", "CapAdd": [ "NET_ADMIN" ]}

   b. ELB setup: External and LB port 9092. native App mode instead of Docker Mode. Note down the DNS name which will be used in Kafka setup next

Kafka Manager setup
	a. Service Setup:
		- Name: kafka-manager
		- Image: duplocloud/kafka:manager_v0
		- Env: { "ZK_HOSTS": "zk-exhibitor-1-kafka.duplopoc.net:2181"}


