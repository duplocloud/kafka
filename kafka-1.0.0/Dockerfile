FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install --yes --no-install-recommends software-properties-common
RUN apt-get install --yes --no-install-recommends curl
RUN apt-get install --yes --no-install-recommends wget
RUN apt-get install --yes python-software-properties
RUN apt-get install --yes --no-install-recommends supervisor
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections &&   apt-get update &&   apt-get install -y software-properties-common &&  add-apt-repository -y ppa:webupd8team/java &&   apt-get update &&   apt-get install -y oracle-java8-installer  &&   rm -rf /var/lib/apt/lists/* &&   rm -rf /var/cache/oracle-jdk8-installer
RUN wget http://www.trieuvan.com/apache/kafka/1.0.0/kafka_2.11-1.0.0.tgz -P /tmp
RUN tar -xvzf /tmp/kafka_2.11-1.0.0.tgz  -C /opt/

ADD server.properties /opt/kafka_2.11-1.0.0/config/server.properties
ADD run_kafka.sh /run_kafka.sh
RUN chmod 777 run_kafka.sh

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /var/log/supervisor
ENTRYPOINT ["/bin/bash", "-c", "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf -n"]
