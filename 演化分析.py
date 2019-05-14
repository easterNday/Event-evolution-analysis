import sqlite3
from 相似度分析 import CalSim
from 基础函数 import *
from LSTM分类器 import *


# 1.1最重要的函数
if __name__ == '__main__':
    # 1.1获取搜索内容
    search = input("搜索内容：")
    # 1.2获取搜索内容的类型
    typ = GetType(input=search)

    # 1.3建立列表存放sql读取结果//可自行增加
    link = []
    title = []
    date = []
    content = []

    # 1.4连接数据库//名字是我随便写的
    initSQL = sqlite3.connect("数据库/分类数据库/测试.db")
    # 1.5从数据库对应类型的表格中获取id, link, title, date, content
    cursor = initSQL.execute(
        "SELECT id, link, title, date, content  from " + typ)
    # 1.6将获得的数据保存到列表中
    for row in cursor:
        # 我没有写ID，别问我为什么，我觉得没用~~~
        link.append(row[1])
        title.append(row[2])
        date.append(row[3])
        content.append(row[4])
    # 1.7关闭数据库
    initSQL.close()

    # 1.7两种演化思路
    # ###############
    # 第一种演化思路 #
    # ###############
    # 1.7.1获取搜索内容类型，根据最高匹配度生成演化图
    # 1.7.1.1获得相似度列表、是0我也豁出去了
    sim = CalSim(doc_test=search, all_docs=title)
    # 1.7.1.2计算最相似标题的相似标题//title[sim[0][0]]最相似标题，title标题表
    fit_list = CalSim(doc_test=title[sim[0][0]],
                      all_docs=title)
    fit = []  # 存放相似主题
    # 1.7.1.3筛选出相似度到达0.8以上的标题
    Similarity_Rate = 0.8  # 定义最小相似度
    for fitter in fit_list:
        if fitter[0] > Similarity_Rate:
            fit.append(title[fitter[0]])
     # 1.7.1.4相似主题去重
    fit = list(set(fit))
    # 1.7.1.5获得相似主题的日期列表
    sort_fit_date = []  # 相似主题的日期列表
    for item in fit:
        sort_fit_date.append(date[title.index(item)])
    # 1.7.1.6相似主题日期去重
    sort_fit_date = list(set(sort_fit_date))
    # 1.7.1.7相似主题排序//这里需要格式化，不然的话可能排序顺序不对，由于我这里的日期都是规定格式的，所以没有特别要求
    sort_fit_date.sort()
    for timer in sort_fit_date:
        print(timer, title[date.index(timer)])

    input("下面的代码不可用，其实用了也没什么，只是还没写好/手动滑稽")
    quit()

    # ###############
    # 第二种演化思路 #
    # ###############
    # 1.7.2.对标题/文本搜索内容进行搜索/相似度匹配//我还没写，因为没想好
    # 相似度匹配按一定相似度大小获得匹配结果可能为0，所以上面写了直接按搜索结果搜索
    # 1.7.2.1打开数据库
    initSQL = sqlite3.connect("数据库/分类数据库/测试.db")
    # 搜索条目
    cursor = initSQL.execute(
        """
        SELECT title
        FROM """ + typ + """
        WHERE title LIKE '%""" + search + """%'
        """)
    # 1.7.2.2存放所有搜索结果
    search_result = []  # 存放搜索结果
    for row in cursor:
        search_result.append("".join(row))
    initSQL.close()  # 关闭数据库
    # 1.7.2.3对search_result逐一进行分析
    for result in search_result:
        pass  # 仍然调用上面的代码、但是数据太多，不知道怎么排布
