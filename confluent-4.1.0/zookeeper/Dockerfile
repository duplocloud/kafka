FROM confluentinc/cp-zookeeper:4.1.0
ADD run.sh /run.sh
RUN chmod 777 /run.sh
RUN apt-get update
RUN pip install logger
ADD launch-zk.py /launch-zk.py
CMD ["/run.sh"]
