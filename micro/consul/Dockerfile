FROM consul:1.5.4

WORKDIR /app

COPY . .

#RUN sudo yum install -y yum-utils
#RUN sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
#RUN sudo yum -y install consul
RUN ls -l

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

#ENTRYPOINT [
#    "consul",
#    "agent",
#    "-server",
#    "-bootstrap",
#    "-ui",
#    "-node=1",
#    "-client=0.0.0.0",
#    "-data-dir=/consul/data",
#    "-config-dir=/consul/config"
#]
