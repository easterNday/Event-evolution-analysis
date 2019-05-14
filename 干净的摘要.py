# 自动摘要
from pyhanlp import *
import pandas as pd
import xlrd
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud

TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")
TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")

# 主函数
if __name__ == '__main__':
    # 1.输入文件
    data_xls = pd.read_excel('词云/涉侨资讯_慈善公益.xlsx')

    # 2.这种方法是因为我用直接读取的方法有点麻烦
    test_data = []
    for i in data_xls.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = data_xls.ix[i, ['title', 'date', 'content']].to_dict()
        test_data.append(row_data)
        # print("最终获取到的数据是：{0}".format(test_data))

    # 3.存放摘要的字典
    dict = []
    guesswhat = ""
    for i in test_data:
        try:
            # print(i['title'], "****",
            #      "".join(HanLP.extractSummary(i['content'], 3)))
            dict.append(
                (i['title'], i['date'], "".join(HanLP.extractSummary(i['content'], 3)), ",".join(HanLP.extractKeyword(i['content'], 5))))
            # 关键字提取
            guesswhat = guesswhat + \
                ",".join(HanLP.extractKeyword(i['content'], 5))
            guesswhat = guesswhat + \
                ",".join(HanLP.extractSummary(i['content'], 3))
        except:
            pass

    # 4.保存为excel
    data_df = pd.DataFrame(dict)
    data_df.columns = ['标题', '日期', '摘要', '关键字']  # 列名称，与dict一样

    # 5.保存为xls
    writer = pd.ExcelWriter('词云/摘要_涉侨资讯_慈善公益.xlsx')
    data_df.to_excel(writer, '你猜我猜不猜', index=False)
    writer.save()

    # 6.生成一个词云图像
    cut_text = " ".join(jieba.cut(guesswhat))
    # 遮罩
    alice_mask = np.array(Image.open("词云/mask.jpeg"))
    cloud = WordCloud(
        # 数值越大、分辨越高
        scale=30,
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=alice_mask,
        # 允许最大词汇
        max_words=2000,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    # 保存
    wCloud.to_file('词云/cloud.jpg')
    # 显示图片
    """
    import matplotlib.pyplot as plt
    plt.imshow(wCloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    """
