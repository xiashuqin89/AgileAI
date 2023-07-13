from nameko.standalone.rpc import ClusterRpcProxy


# MQ配置
config_mq = {'AMQP_URI': "amqp://admin:admin@ip地址:5672/my_vhost"}


with ClusterRpcProxy(config_mq) as rpc:
    # 消费者调用微服务(生产者)，获取服务（生产者）的返回值
    result = rpc.generate_service.hello_world(msg="xag msg")
    # 返回结果
    print(result, 200)
