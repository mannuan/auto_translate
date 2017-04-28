import http.client
import hashlib
import urllib
from urllib import parse
import random
import json


class Translater(object):
    # 百度翻译 翻译句子或单词
    def __init__(self, appid, secret_key, from_lang='en', to_lang='zh'):
        self.appid = appid
        self.secretKey = secret_key
        self.httpClient = None
        self.myurl = '/api/trans/vip/translate'
        self.fromLang = from_lang
        self.toLang = to_lang
        self.salt = random.randint(32768, 65536)

    def translate(self, sentence):
        sign = self.appid + sentence + str(self.salt) + self.secretKey
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        self.myurl = self.myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(
            sentence) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(self.salt) + '&sign=' + sign

        try:
            self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            self.httpClient.request('GET', self.myurl)
            # response是HTTPResponse对象
            response = self.httpClient.getresponse()
            print()
            if response.getcode() == 200:
                result = response.read().decode('utf-8')
                s = json.loads(result)
                return True, s['trans_result'][0]['dst']
            else:
                return False, "error"
        except Exception as e:
            print(type(e), e)
            return False, "exception"
        finally:
            if self.httpClient:
                self.httpClient.close()


if __name__ == '__main__':
    se = "R E S EARCH M ETHOD."
    translater = Translater('20170428000045860', 'fJGtM45dsfrRcfCovf64')
    res = translater.translate(se)
    print(res)
