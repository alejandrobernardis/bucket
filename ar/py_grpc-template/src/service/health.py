import health_pb2
import health_pb2_grpc


class HealthApi(health_pb2_grpc.HealthServiceServicer):
    async def Ping(self, request, context):
        return health_pb2.Response(message='Pong')

    async def Health(self, request, context):
        return health_pb2.Response(message='Ok')
