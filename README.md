Zookeepeer Installation Steps

1. EC2 Instance Setup
	a. Create a t2.large instance with 
		- Host volume mappings as [{"Name": "/dev/xvdf", "VolumeType": "io1", "Size": "100", "Iops": "1000"}]
		- Allocation tag as zk-exhibitor-1
	b. Login to the ec2 instance and run
		- mkfs -t ext4 /dev/xvdf
		- mkdir /mnt/zkdata1
		- edit /etc/rc.local and before the line exit 0 add mount /dev/xvdf /mnt/zkdata1
		- reboot and login to validate that df -h shows /dev/xbdf mounted
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

   b. ELB setup: External and LB port 2181. native App mode instead of Docker Mode. Note down the DNS name which will be used in Kafka setup next


Kafka Installation Steps

1. EC2 Instance Setup
	a. Create a m4.large instance with 
		- Host volume mappings as [{"Name": "/dev/xvdf", "VolumeType": "st1", "Size": "500", "Iops": null}]
		- Allocation tag as kafka-101
	b. Login to the ec2 instance and edit /etc/rc.local and before the line exit 0 add 
	    mkdir -p /mnt/kafkadata1
		mount /dev/xvdf /mnt/kafkadata1 -o noatime
		sysctl vm.swappiness=1
		sysctl vm.dirty_background_ratio=5
		sysctl vm.dirty_ratio=60 
	c. Reboot and login to validate that df -h shows /dev/xbdf mounted

3. Microservice setup
   a. Service Setup:
   	- Name: kafka-101
   	- Image: duplocloud/kafka:kafka_v2
   	- Env: { "JMX_PORT": 9999, "ZOOKEEPER_HOSTS":"<dnsname>:2181", "HOST_SUFFIX":".<dnsdomain>" } where dns name is shown in the column called dns in the services tab next to the service zk-exhibitor-1 (for example zk-exhibitor-1-kafka.duplopoc.net) where domainsuffix is the part of the dns name after zk-exhibitor-1 (for example -kafka.duplopoc.net assuming kafka is the name of the duplo tenant). Basically domainsuffix is part of the dns name that is constant for all services within the tenant. Typically it is "-<tenantname>.<domainoftheorg>" where domainoftheorg is constant per duplo deployment.
   	- Allocation tag: kafka-101
   	- Volume Mount: "/mnt/kafkadata1:/mnt/kafkadata1"
   	- Docker Host config: {"NetworkMode": "host", "CapAdd": [ "NET_ADMIN" ]}

   b. ELB setup: External and LB port 9092. native App mode instead of Docker Mode. Note down the DNS name which will be used in Kafka setup next



