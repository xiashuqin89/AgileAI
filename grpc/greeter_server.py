from concurrent import futures
import logging
import signal

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

import _credentials
import _consul

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

_LISTEN_ADDRESS_TEMPLATE = 'localhost:%d'
_SIGNATURE_HEADER_KEY = 'x-signature'


class SignatureValidationInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid signature')
        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method.split('/')[-1]
        expected_metadata = (_SIGNATURE_HEADER_KEY, method_name[::-1])
        if expected_metadata in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._abortion


def _unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)
    return grpc.unary_unary_rpc_method_handler(terminate)


class RequestHeaderValidatorInterceptor(grpc.ServerInterceptor):
    def __init__(self, header, value, code, details):
        self._header = header
        self._value = value
        self._terminator = _unary_unary_rpc_terminator(code, details)

    def intercept_service(self, continuation, handler_call_details):
        if (self._header,
                self._value) in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._terminator


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        # metadata
        for key, value in context.invocation_metadata():
            print('Received initial metadata: key=%s value=%s' % (key, value))

        context.set_trailing_metadata((
            ('checksum-bin', b'I agree'),
            ('retry', 'false'),
        ))
        return helloworld_pb2.HelloReply(message=f'Hello again, {request.name}!')


def stop_serve(signum, frame):
    print("process killed ！！！！")
    _consul.unregister(service_id='hello-localhost-50051')
    raise KeyboardInterrupt


def serve():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=(SignatureValidationInterceptor(),))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server_credentials = grpc.ssl_server_credentials(((
        _credentials.SERVER_CERTIFICATE_KEY,
        _credentials.SERVER_CERTIFICATE,
    ),))
    # server.add_insecure_port('[::]:' + port)
    server.add_secure_port(f'[::]:{port}', server_credentials)
    _consul.register('hello', 'localhost', port)
    server.start()
    signal.signal(signal.SIGINT, stop_serve)
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
