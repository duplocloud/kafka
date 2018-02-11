FROM openjdk:8

RUN wget --progress=dot:mega http://apache.claz.org/kafka/0.11.0.2/kafka_2.11-0.11.0.2.tgz
RUN tar xzf kafka_2.11-0.11.0.2.tgz
RUN mv kafka_2.11-0.11.0.2 /kafka
WORKDIR /kafka
ADD ./scripts /scripts

CMD "/scripts/start-kafka.py"
