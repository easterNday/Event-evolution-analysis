from pyhanlp import *
import pandas as pd

TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")

if __name__ == "__main__":
    # 1.输入文件
    data_xls = pd.read_excel('词云/法国新闻.xlsx')

    # 2.这种方法是因为我用直接读取的方法有点麻烦
    test_data = []
    for i in data_xls.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = data_xls.loc[i, ['链接','新闻', '日期','来源', '内容']].to_dict()
        test_data.append(row_data)
    print("最终获取到的数据是：{0}".format(test_data))

    # 3.存放摘要的字典
    dict = []
    index = 0
    for i in test_data:
        try:
            # 此处replace将英文冒号替换为中文冒号、是为了防止绘制图时候出现Warning
            dict.append((i['日期'], i['新闻'],  i['内容'],i["链接"]))
            # dict.append((i['date'].replace(':', '：').strip(), str(index),  "".join(HanLP.extractSummary(i['content'], 3))))#序号
            index = index + 1
        except:
            pass
    dict.sort()  # 按照时间排序

    #5.生成综述
    #5.1第一种综述
    #5.1.1合并内容,速度慢且内容杂，不建议使用
    #content_All = "\n".join([i[2] for i in dict])
    #print(content_All)
    #News = HanLP.extractSummary(content_All, 20)
    #print(News)

    #5.2第二种综述
    #Suammaries = [("\t"+ i[0][:10] + "。".join(HanLP.extractSummary(i[2],3)).strip()) for i in dict if i[0] > '2018']
    #content_All = "\n".join(Suammaries)
    #print(content_All)

    #5.3第三种综述
    #Suammaries = [("\t"+ i[0][:7] + "。".join(HanLP.extractSummary(i[2],3)).strip()) for i in dict if i[0] > '2018' and]
    content = ""
    for i in dict:
        if i[0][:7] in content:
            content = content + "\t" + i[3]  + ",".join(HanLP.extractSummary(i[2],3)) + "\r\n"
        else:
            content = content + "\r\n" +  "".join(i[0][:7])+ "\r\n\t" + i[3] + ",".join(HanLP.extractSummary(i[2],3)).strip() + "\r\n"
    print(content)

