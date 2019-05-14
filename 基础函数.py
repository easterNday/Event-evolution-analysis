import jieba

# 1.定义的Type列表，可以对应数字查询所属类别
TypeTable = ("教育", "人物", "行政", "经济", "政策")


# 2.LSTM生成时的预定义变量
MAX_SEQUENCE_LENGTH = 100  # 最大序列长度
EMBEDDING_DIM = 200  # embdding 维度
VALIDATION_SPLIT = 0.16  # 验证集比例
TEST_SPLIT = 0.2  # 测试集比例


# 3.停用词表获取
def getStopWords():
    # 加载停用词,从网上下载的停词表//可以调用其它的模块直接获得分词表
    stopwords = []
    file = open("停词表/stopwords.txt")  # 本地分词文件
    for line in file:
        stopwords.append(line.strip('\n'))
    file.close()
    return stopwords


# 4.处理输入文本
def Just_text(text):
    stopwords = getStopWords()
    segs = jieba.lcut(text)
    segs = [v for v in segs if not str(v).isdigit()]  # 去数字
    segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
    segs = list(filter(lambda x: len(x) > 1, segs))  # 长度为1的字符
    segs = list(
        filter(lambda x: x not in stopwords, segs))  # 去掉停用词
    return " ".join(segs)
