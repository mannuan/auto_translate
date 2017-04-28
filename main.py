# 自动翻译

from auto_translate import readers, translater, outputers


class MyTranslater(object):
    def __init__(self, in_pdf_path, out_txt_path, out_html_path, name):
        self.translaters = list()
        self.reader = readers.PDFReader(in_pdf_path + name + ".pdf", out_txt_path + name + '.txt')
        self.outputer = outputers.HTMLOutPuter()
        self.out_html_path = out_html_path + name + ".html"

    def add_account(self, appid, secret_key):
        # 添加一个翻译器
        self.translaters.append(translater.Translater(appid, secret_key))

    def process(self):
        self.reader.read()
        count = 1
        datas = list()
        current_translater = self.translaters.pop()
        while self.reader.has_next_sentence():
            # 读取一行句子
            sentence = self.reader.next_sentence()
            # 翻译
            ok, result = current_translater.translate(sentence)
            if not ok:
                # 翻译失败,换一个实例
                try:
                    current_translater = self.translaters.pop()
                except:
                    break
                ok, result = current_translater.translate(sentence)
            # 如果翻译成功, 则添加
            data = dict()
            data['count'] = count
            data['original'] = sentence
            data['translation'] = result
            datas.append(data)
            count += 1
            # if count == 5:
            #     break0
            print(data['count'], data['translation'])
        self.outputer.write(self.out_html_path, datas)
        print("翻译句子---------completed")


if __name__ == '__main__':
    # 翻译
    n = "20"
    t = MyTranslater('pdfs/', 'txts/', 'htmls/', n)
    t.add_account('20151113000005349', 'osubCEzlGjzvw8qdQc41')
    # 如果文档很大的话,就要多些帐号
    # 因为百度翻译API有限制
    t.process()
    print("end")
