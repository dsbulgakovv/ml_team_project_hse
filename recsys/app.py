from fastapi import FastAPI
from fastapi.responses import JSONResponse
import grpc
from concurrent import futures
from proto import service_pb2_grpc, service_pb2  # TODO добавить компиляцию в докерфайл

app = FastAPI()


class YourService(service_pb2_grpc.YourServiceServicer):
    def SayHello(self, request, context):
        return service_pb2.HelloResponse(message=f"Hello, {request.name}!")


def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_YourServiceServicer_to_server(YourService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


@app.get('/')
def hello():
    return JSONResponse(content={"message": "Hello, world!"})


if __name__ == '__main__':
    import threading
    grpc_thread = threading.Thread(target=run_grpc_server)
    grpc_thread.start()
    uvicorn_command = "uvicorn your_script_name:app --host 0.0.0.0 --port 8000 --reload"
    import os
    os.system(uvicorn_command)