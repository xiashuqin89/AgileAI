FROM python:3.10.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

# 注册服务
# producer_service：目标文件
# admin:admin：MQ用户名及密码
# ip地址:5672：MQ服务器ip地址及应用端口号
# my_vhost：虚拟机名
# nameko run producer_service --broker amqp://admin:admin@ip地址:5672/my_vhost

ENTRYPOINT ["nameko", "run", "main", "--broker", "amqp://admin:admin@ip地址:5672/my_vhost"]
