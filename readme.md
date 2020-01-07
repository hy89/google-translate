### 文件目录说明
core目录内是google翻译的核心代码

rpc_server内的`server.py`是rpc的服务端,在其中调用core目录内的代码

`rpc_conf.py`是rpc的配置代码

`rpc_client.py`是rpc客户端的测试代码,可参考其中代码自实现该代码

### 运行
- 1.运行rpc_server内的`server.py`启动rpc服务
- 2.运行`rpc_client.py`进行测试rpc服务是否运行正常

### 调用rpc翻译服务需要传递的参数说明
需要传递一个字典,具体可见`rpc_client.py`中代码,该处对字典进行说明:
```python
translate_word = {'src': 'zh-CN', 'dest': 'en', 'content': content, 'cookies': cookies}
# content 要翻译的内容
# cookies google返回的cookies
# src 原文语言
# dest 目标语言
# 常用语言说明  中文 zh-CN，英文：en，日文：ja，韩文：ko
```


### 一些问题
- google翻译支持5000字符的翻译量(实测没有这么多)
- 翻译过程中可能会出现反爬导致异常,捕获异常跳过本次翻译仍可继续运行
- google的cookies时间较长,一般情况下无需多次获取该值
- google响应结果中可能会出现<em></em></ em>标签, 注意处理

