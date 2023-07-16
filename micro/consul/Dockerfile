#FROM tencentos/tencentos_server24_mini:latest
#
#WORKDIR /app
#
#COPY . .
#
#RUN yum install -y yum-utils
#RUN yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
#RUN yum -y install consul
#
#RUN rm -f /etc/localtime \
#&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
#&& echo "Asia/Shanghai" > /etc/timezone


FROM consul:latest

CMD ["consul agent -data-dir=/consul/data -config-dir=/consul/config -server -bootstrap -ui -node=1 -client=0.0.0.0"]