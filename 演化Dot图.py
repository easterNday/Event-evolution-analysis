import os
from graphviz import Digraph
from 相似度分析 import CalSim
from pyhanlp import *
import pandas as pd
import xlrd
import jieba
import graphviz

TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")
# TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")

# 添加环境变量graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


# 比较相似度然后生成连接dot的函数
def getSimilar(list=[], node=[]):
    # list为输入的数据、node是为了防止插入dot时重复，筛选用的

    # 要比较的列表、从1开始切片，这样的的话有效去除了相似度最高的自己
    summaries = [i[2] for i in list[1:]]
    # 相似度表格
    SimTab = CalSim(list[0][2], summaries)

    # 如果相似表格不为空
    if SimTab:
        # list中第一个元素加入节点
        dot.node(list[0][1], list[0][1])  # 标题、序号
        # dot.node(list[0][0] + list[0][1], list[0][0] + list[0][1])  # 时间标题

    # 这个地方原本逻辑有一点问题，我也不知道怎么想的，可能还有问题（后续）
    # 选取相似度最高的六个数据（除去本身）
    for sim in SimTab[:3]:
        # 相似度高于0、这行可以去掉，因为有时候相似度很低
        if sim[1] > 0:
            # 如果不存在节点，就生成一个节点
            if (not list[sim[0]][1] in node) and list[sim[0]:]:
                dot.node(list[sim[0]][1], list[sim[0]][1])  # 标题、序号
                # dot.node(list[sim[0]][0] + list[sim[0]][1],list[sim[0]][0] + list[sim[0]][1])  # 时间标题
                node.append(list[sim[0]][1])
                # 在创建两圆点之间创建一条边
                dot.edge(list[0][1], list[sim[0]][1], str(sim[1]))  # 标题、序号
                # dot.edge(list[0][0] + list[0][1], list[sim[0]][0] + list[sim[0]][1], str(sim[1]))  # 时间标题
                # 如果后面还有数据
                if list[sim[0]:]:
                    getSimilar(list=list[sim[0]:], node=node)


# 主函数
if __name__ == '__main__':
    # 1.输入文件
    data_xls = pd.read_excel('词云/爬取内容.xlsx')

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
            dict.append((i['日期'].replace(':', '：').strip(), i['新闻'].replace(
                ':', '：').strip(),  "".join(HanLP.extractSummary(i['内容'], 3))))
            # dict.append((i['date'].replace(':', '：').strip(), str(index),  "".join(HanLP.extractSummary(i['content'], 3))))#序号
            index = index + 1
        except:
            pass
    dict.sort()  # 按照时间排序

    # 4.摘要
    summaries = [i[2] for i in dict]

    # 5.画图
    dot = Digraph(comment='不朽香江名句')
    node = []  # 筛选节点列表
    # 5.1生成节点
    getSimilar(dict[:], node)
    # 5.2获取DOT source源码的字符串形式
    dot_data = list(dot)
    # 5.3添加中文显示，不然显示乱码
    Chinese_foramt = ["\trankdir=LR",  # 输出方向LR\RL\BT\TB
                      "\trotate=0",  # 旋转角度

                      # 字体设置，防止乱码
                      '\tfontname="Microsoft YaHei"',
                      '\tedge [fontname="Microsoft YaHei"];',
                      '\tnode [fontname="Microsoft YaHei"];']
    dot_data = dot_data[:2] + Chinese_foramt + dot_data[2:]
    dot = graphviz.Source("\r\n".join(dot_data))

    # print(dot.source)
    # dot.view() # 显示图片
    # 5.5保存source到文件，并提供Graphviz引擎
    dot.render('演化图/蓝皮书演化图.gv', view=True)
