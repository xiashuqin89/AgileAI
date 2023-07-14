import socket

import consul


def register(server_name, ip, port: int):
    c = consul.Consul(host='127.0.0.1', port=8500)  # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
    print(f"GRPC开始注册服务{server_name}")
    check = consul.Check.tcp(ip, port, "10s")  # 健康检查的ip，端口，检查时间
    if c.agent.service.register(name=server_name,
                                service_id=f'{server_name}-{ip}-{port}',
                                address=ip,
                                port=port,
                                check=check):  # 注册服务部分
        print(f"GRPC注册服务{server_name}成功")
    else:
        print(f"GRPC注册服务{server_name}失败")


def unregister(service_id):
    c = consul.Consul()
    print(f"开始退出服务{service_id}")
    if c.agent.service.deregister(service_id=service_id):
        print(f"GRPC注销服务{service_id}成功")
    else:
        print(f"GRPC注销服务{service_id}失败")


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def get_service(server_name):
    c = consul.Consul(host='127.0.0.1', port=8500)
    _, nodes = c.health.service(service=server_name)
    if len(nodes) == 0:
        raise Exception('service is empty.')
    for node in nodes:
        service = node.get('Service')
        return service['Address'], service['Port']
