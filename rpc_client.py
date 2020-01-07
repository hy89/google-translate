# @Author: hy
# @Time: 2019-11-15 10:20

import json
import time

import grpc
from rpc_server.fanyi import fanyi_pb2, fanyi_pb2_grpc
from rpc_conf import PORT, HOST
from core import google


def tr(n):
    # print('n-->', n)
    conn = grpc.insecure_channel(HOST + ':' + PORT)
    client = fanyi_pb2_grpc.TranslateStub(channel=conn)
    response = client.DoTranslate(fanyi_pb2.Data(text=json.dumps(n)))
    # print("received: " + response.text)  # 打印接受到的响应信息
    conn.close()
    return response.text


if __name__ == '__main__':
    # 以下为测试服务的客户端代码
    cookies = google.get_cookies()  # 获取cookies，网页得到的expires时间有半年之久
    content = "hello"
    # src是源文本语言，dest为要翻译成的语言，content为要翻译的文本
    # 中文 zh-CN，英文：en，日文：ja，韩文：ko
    try:
        ret = tr({'src': 'zh-CN', 'dest': 'en', 'content': content, 'cookies': cookies})  # 翻译成英文
        time.sleep(0.5)
    except Exception as e:
        # 一般都是连接超时的错误，翻译失败的源数据如何处理由客户端自定义
        print('翻译失败', e)
