FROM hashicorp/consul:1.15.4

WORKDIR /app

COPY . .

RUN ls -l

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

ENTRYPOINT [
    "consul",
    "agent",
    "-server",
    "-bootstrap",
    "-ui",
    "-node=1",
    "-client=0.0.0.0",
    "-data-dir=/consul/data",
    "-config-dir=/consul/config"
]
