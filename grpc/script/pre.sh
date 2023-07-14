python -m grpc_tools.protoc -I ./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/helloworld.proto

docker run -d -p 8500:8500 --restart=always --name=consul consul:1.15.4 agent -server -bootstrap -ui -node=1 -client='0.0.0.0'