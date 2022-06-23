import common_pb2
import common_pb2_grpc


class CommonApi(common_pb2_grpc.CommonServiceServicer):
    async def Version(self, request, context):
        return common_pb2.Response(message='v1.0.0')
