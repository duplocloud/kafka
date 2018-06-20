FROM openjdk:8

RUN wget --progress=dot:mega http://apache.claz.org/kafka/1.0.0/kafka_2.11-1.0.0.tgz
RUN tar xzf kafka_2.11-1.0.0.tgz
RUN mv kafka_2.11-1.0.0 /kafka
WORKDIR /kafka
ADD ./scripts /scripts

CMD "/scripts/start-kafka.py"
