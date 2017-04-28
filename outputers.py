import os


class HTMLOutPuter(object):

    def write(self, out_html_path, datas):
        # 如果txt文件存在就删除
        if os.path.exists(out_html_path):
            os.remove(out_html_path)
        fout = open(out_html_path, 'w')
        fout.write('<html>')
        fout.write('<head>')
        fout.write('<meta charset="UTF-8">')
        fout.write('</head>')
        fout.write('<body>')
        fout.write('<ul>')

        for data in datas:
            fout.write('<li>%d: %s</li>' % (data['count'], data['original']))
            fout.write('<li style="list-style: none">    %s</li><br>' % data['translation'])

        fout.write('</ul>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
        print("输出html文件: %s ---------completed" % out_html_path)
