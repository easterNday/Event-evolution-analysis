import jieba
from gensim import corpora, models, similarities


# 1.将文本集合转化为词向量集合
def SearlizeDoc(all_doc):
    all_doc_list = []
    for doc in all_doc:
        doc_list = [word for word in jieba.cut(doc)]
        all_doc_list.append(doc_list)
    return all_doc_list


# 2.计算相似度函数
def CalSim(doc_test, all_docs):
    # 2.1转化的词向量集合
    all_doc_list = SearlizeDoc(all_docs)
    # 2.2待分析的句子
    doc_test_list = [word for word in jieba.cut(doc_test)]

    # 2.3词向量字典
    dictionary = corpora.Dictionary(all_doc_list)
    # 词袋中用数字对所有词进行了编号dictionary.keys()
    # 编号与词之间的对应关系dictionary.token2id

    # 2.4使用doc2bow制作语料库
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]

    # 2.5用同样的方法，把测试文档也转换为二元组的向量
    doc_test_vec = dictionary.doc2bow(doc_test_list)

    # 2.6使用TF-IDF模型对语料库建模
    tfidf = models.TfidfModel(corpus)

    # 2.7对每个目标文档，分析测试文档的相似度
    # 获取测试文档中，每个词的TF-IDF值 tfidf[doc_test_vec]
    index = similarities.SparseMatrixSimilarity(
        tfidf[corpus], num_features=len(dictionary.keys()))

    # 2.8相似度列表
    sim = index[tfidf[doc_test_vec]]
    Simlatity = sorted(enumerate(sim), key=lambda item: -item[1])

    return Simlatity
