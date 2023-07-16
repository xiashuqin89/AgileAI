from __future__ import print_function

import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

import _credentials
import _consul

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


_SERVER_ADDR_TEMPLATE = 'localhost:%d'
_SIGNATURE_HEADER_KEY = 'x-signature'


class AuthGateway(grpc.AuthMetadataPlugin):

    def __call__(self, context, callback):
        """Implements authentication by passing metadata to a callback.

        Implementations of this method must not block.

        Args:
          context: An AuthMetadataContext providing information on the RPC that
            the plugin is being called to authenticate.
          callback: An AuthMetadataPluginCallback to be invoked either
            synchronously or asynchronously.
        """
        # Example AuthMetadataContext object:
        # AuthMetadataContext(
        #     service_url=u'https://localhost:50051/helloworld.Greeter',
        #     method_name=u'SayHello')
        signature = context.method_name[::-1]
        # NOTE: The metadata keys provided to the callback must be lower-cased.
        callback(((_SIGNATURE_HEADER_KEY, signature),), None)


def unary_call(stub: helloworld_pb2_grpc.GreeterStub, request_id: int,
               message: str):
    print("call:", request_id)
    try:
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=message),
                                 timeout=3)
        print(f"Greeter client received: {response.message}")
    except grpc.RpcError as rpc_error:
        print(f"Call failed with code: {rpc_error.code()}")


def send_rpc(address, port):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel(f'{address}:{port}') as channel:
        unary_call(helloworld_pb2_grpc.GreeterStub(channel), 1, 'you')


def send_rpc_with_auth(address, port):
    call_credentials = grpc.metadata_call_credentials(AuthGateway(),
                                                      name='auth gateway')
    channel_credential = grpc.ssl_channel_credentials(_credentials.ROOT_CERTIFICATE)
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    with grpc.secure_channel(f'{address}:{port}', composite_credentials) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        try:
            response = stub.SayHello(request)
            print("Greeter client received: " + response.message)
        except grpc.RpcError as rpc_error:
            _LOGGER.error('Received error: %s', rpc_error)
            return rpc_error
        else:
            _LOGGER.info('Received message: %s', response)
            return response


def run():
    address, port = _consul.get_service('hello')
    send_rpc_with_auth(address, port)


if __name__ == '__main__':
    logging.basicConfig()
    run()
