# __author__ = 'heyin'
# __date__ = '2019/2/14 16:03'
# google翻译rpc服务端代码
import sys

sys.path.append('../')
import json

import grpc
import time
from concurrent import futures
from rpc_server.fanyi import fanyi_pb2, fanyi_pb2_grpc
from rpc_conf import HOST, PORT, ONE_DAY_IN_SECONDS
from core import google

js = google.Py4Js()


class Translate(fanyi_pb2_grpc.TranslateServicer):
    def DoTranslate(self, request, context):
        args = request.text
        args = json.loads(args)
        src = args.get('src')
        dest = args.get('dest')
        cookies = args.get('cookies')

        # 下边内容为谷歌的翻译操作
        ret = google.translate(js, args.get('content'), src, dest, cookies)
        return fanyi_pb2.Data(text=ret)


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    fanyi_pb2_grpc.add_TranslateServicer_to_server(Translate(), grpcServer)
    grpcServer.add_insecure_port(HOST + ':' + PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    serve()
