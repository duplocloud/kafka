FROM confluentinc/cp-kafka:4.1.0
ADD run.sh /run.sh
RUN chmod 777 /run.sh
RUN apt-get update
RUN pip install logger
ADD launch-kafka.py /launch-kafka.py
CMD ["/run.sh"]
