FROM hashicorp/consul:latest
WORKDIR /app
RUN cd /app
ENTRYPOINT ["consul", "agent", "-data-dir=/consul/data", "-config-dir=/consul/config", "-server", "-bootstrap", "-ui", "-node=1", "-client=0.0.0.0", "-bind=127.0.0.1"]