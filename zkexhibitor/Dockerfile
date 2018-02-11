#### Build exhibitor jar
FROM openjdk:8 as builder

RUN apt-get update && apt-get -y install ca-certificates

RUN apt-get -y install maven &&\
  mkdir /exhibitor &&\
  cd /exhibitor

ADD pom.xml /exhibitor/pom.xml

RUN cd /exhibitor &&\
  mvn assembly:single &&\
  mv target/exhibitor-1.0-jar-with-dependencies.jar . &&\
  rm -rf /exhibitor/target &&\
  rm /exhibitor/pom.xml

##### Build main image

FROM openjdk:8

RUN mkdir /exhibitor
COPY --from=builder /exhibitor/exhibitor-1.0-jar-with-dependencies.jar /exhibitor

RUN apt-get update
RUN apt-get -y install ca-certificates
RUN apt-get -y upgrade
RUN apt-get -y install vim curl supervisor

RUN wget -q http://archive.apache.org/dist/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz.md5
RUN wget -q http://archive.apache.org/dist/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz
RUN md5sum -c zookeeper-3.4.6.tar.gz.md5
RUN mkdir -p /zookeeper/lib/
RUN mkdir -p /zookeeper/zkdata/
RUN ln -s /mnt/zkdata1/zklogs/ /zookeeper/


WORKDIR /zookeeper/lib/
RUN tar xzf /zookeeper-3.4.6.tar.gz
RUN rm /zookeeper-3.4.6.tar.gz*

WORKDIR /exhibitor
ADD run_exhibitor.sh .
ADD supervisord.conf .

EXPOSE 2181 2888 3888 8080
CMD ["/usr/bin/supervisord", "-c", "supervisord.conf", "-n"]
