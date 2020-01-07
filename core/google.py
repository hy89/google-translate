# google翻译的核心代码
import requests
import json
import execjs  # 必须，需要先用pip 安装，用来执行js脚本
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("google_log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
        };      
        function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
        } 
        """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def get_cookies():
    header = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
    ret = requests.get('https://translate.google.cn/', headers=header, timeout=5.0)
    nid = ret.cookies.get('NID')
    cookies = {'NID': nid}
    return cookies


def buildUrl(text, tk, src, dest):
    baseUrl = 'https://translate.google.cn/translate_a/single'
    baseUrl += '?client=webapp&'
    baseUrl += 'sl=%s&' % src  # 英文转中文
    baseUrl += 'tl=%s&' % dest
    baseUrl += 'hl=zh-CN&'
    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    # baseUrl += 'source=btn&'
    # baseUrl += 'ssel=0&'
    # baseUrl += 'tsel=0&'
    # baseUrl += 'kc=0&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'q=' + text
    return baseUrl


def translate(js, text, src, dest, cookies):
    """
    翻译接口
    :param js: js对象
    :param text: 文本内容
    :param src: 源语言
    :param dest: 目标语言
    :return:
    """
    header = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
    url = buildUrl(text, js.getTk(text), src, dest)

    # try:
    r = requests.get(url, headers=header, timeout=10.0, cookies=cookies)  # 连接超时异常由客户端接收处理
    result = json.loads(r.text)
    # print(result)
    if result[7] != None:
        # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
        try:
            correctText = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
            # print(correctText)
            correctUrl = buildUrl(correctText, js.getTk(correctText), src, dest)
            correctR = requests.get(correctUrl)
            newResult = json.loads(correctR.text)
            res = newResult[0][0][0]
        except Exception as e:
            # print("错误信息1-->:%s" % e)
            logger.error("错误信息1-->:%s" % e)
            res = result[0][0][0]
    else:
        sentences = result[0]
        res = ''
        for s in sentences[:-1]:
            res += s[0]

    # except Exception as e:
    #     # print('url-->', url)
    #     res = ''
    #     # print("错误信息:", e)
    #     logger.error("错误信息2==>:%s" % e)
    # finally:
    return res


if __name__ == '__main__':
    js = Py4Js()

    cookies = get_cookies()
    for i in range(1000):
        print('i--->>>', i)
        try:
            res = translate(js, '最近，有个师妹问我来到美国最大的收获是什么，我想了想，“保持一个开放的心态，随时根据形势，做出相应调整”。', 'zh-CN', 'en', cookies)
            print('first--', res)
            res = translate(js, res, 'en', 'zh-CN', cookies)
            print('second--', res)
        except Exception as e:
            print(e)
