import os
import sys
import importlib
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class PDFReader(object):
    def __init__(self, in_pdf_path, out_txt_path):
        self.sentences = list()
        self.in_pdf_path = in_pdf_path
        self.out_txt_path = out_txt_path

    def has_next_sentence(self):
        return len(self.sentences) != 0

    def next_sentence(self):
        if self.has_next_sentence():
            return self.sentences.pop()
        return None

    def _convert_pdf_txt(self):
        # 开始读取文件
        fp = open(self.in_pdf_path, 'rb')  # 以二进制读模式打开
        # 用文件对象来创建一个pdf文档分析器
        praser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器 与文档对象
        praser.set_document(doc)
        doc.set_parser(praser)

        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 创建PDf 资源管理器 来管理共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # 如果txt文件存在就删除
            if os.path.exists(self.out_txt_path):
                os.remove(self.out_txt_path)
            # 循环遍历列表，每次处理一个page的内容
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象
                # 里面存放着 这个page解析出的各种对象
                # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
                # 想要获取文本就获得对象的text属性，
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        with open(self.out_txt_path, 'a') as f:
                            results = x.get_text()
                            for line in results.split('.'):
                                line.strip()
                                temp = line.replace('\n', ' ')
                                # print("===>", temp.strip())
                                # # print("=", len(temp))
                                # # print("=", len(temp.strip()))
                                # print("--", temp.strip() + '.\n')
                                f.write(temp.strip() + '.\n')
                            f.write("#\n")

    def _read_txt_file(self):
        with open(self.out_txt_path, 'r') as file:
            for line in file:
                if self._is_eligibled(line):
                    self.sentences.append(line.strip())
        self.sentences.reverse()

    def _is_eligibled(self, line):
        c = line.strip()[0]
        if not c.isupper():
            return False
        if len(line) < 20:
            return False
        return True

    def read(self):
        # 1. pdf 转化为 txt
        self._convert_pdf_txt()
        # 2. 读取 txt 文件
        self._read_txt_file()
        print("读取pdf文件---------completed")


if __name__ == '__main__':
    n = '33'
    reader = PDFReader("pdfs/" + n + ".pdf", "txts/" + n + ".txt")
    reader.read()
    count = 1
    while reader.has_next_sentence():
        # print(count, reader.next_sentence())
        reader.next_sentence()
        count += 1


