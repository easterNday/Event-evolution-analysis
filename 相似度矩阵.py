from 相似度分析 import CalSim
from pyhanlp import *
import pandas as pd
import xlrd
import jieba

TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")
TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")

# 主函数
if __name__ == '__main__':
    # 1.输入文件
    data_xls = pd.read_excel('词云/精简华人华侨蓝皮书.xls')

    # 2.这种方法是因为我用直接读取的方法有点麻烦
    test_data = []
    for i in data_xls.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = data_xls.ix[i, ['title', 'date', 'content']].to_dict()
        test_data.append(row_data)
        # print("最终获取到的数据是：{0}".format(test_data))

    # 3.存放摘要的字典
    dict = []
    for i in test_data:
        try:
            # print(i['title'], "****",
            #      "".join(HanLP.extractSummary(i['content'], 3)))
            dict.append(
                (i['title'], i['date'], "".join(HanLP.extractSummary(i['content'], 3)), ",".join(HanLP.extractKeyword(i['content'], 5))))
        except:
            pass
    # 4.摘要集合
    summaries = [i[2] for i in dict if i[2] != '']
    # 5.计算相似度
    Similarities_All = []
    for summ in summaries:
        # 计算相似度
        AllSim = CalSim(summ, summaries)
        # 排序相似度
        AllSim.sort()
        Similarities_All.append(AllSim)

    # 6.保存为excel
    data_df = pd.DataFrame(Similarities_All)
    data_df.columns = summaries
    data_df.index = summaries
    writer = pd.ExcelWriter('矩阵/矩阵_精简华人华侨蓝皮书.xlsx')
    data_df.to_excel(writer, '你猜我猜不猜', index=True)
    writer.save()
