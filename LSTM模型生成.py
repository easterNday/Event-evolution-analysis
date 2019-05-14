# 引入包
from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM, Embedding, GRU
from keras.layers import Dense, Input, Flatten, Dropout
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
import random
import jieba
import pandas as pd
import numpy as np


# 这里会有一些预设变量，我存在了基础函数里面，会在第3点用到
# 预定义变量，此处方便观看
# MAX_SEQUENCE_LENGTH = 100  # 最大序列长度
# EMBEDDING_DIM = 200  # embdding 维度
# VALIDATION_SPLIT = 0.16  # 验证集比例
# TEST_SPLIT = 0.2  # 测试集比例
# 最大序列长度——pad生成data的最大数量，测试时为100，此处可以调大，使模型更可靠
# Embdding维度——我也不知道有什么用，总之越大越好
# 验证集比例——在模型训练的时候会用输入所有数据按比例划分最后一部分的数据验证模型的可靠性
# 测试集比例——此处为用于测试的，可以设置为0，则上面两项可以调大


# 获取停词表//已经卸载基础函数里面了
from 基础函数 import *
stopwords = getStopWords()


# 1.已经标注好的语料输入
# 1.1加载语料（可以按照分类加载、此处自己编写）
教育_df = pd.read_csv('训练集/教育.csv', encoding='utf-8', sep=',')
人物_df = pd.read_csv('训练集/人物.csv', encoding='utf-8', sep=',')
行政_df = pd.read_csv('训练集/行政.csv', encoding='utf-8', sep=',')
经济_df = pd.read_csv('训练集/经济.csv', encoding='utf-8', sep=',')
政策_df = pd.read_csv('训练集/政策.csv', encoding='utf-8', sep=',')
# 1.2删除语料的nan行
教育_df.dropna(inplace=True)
人物_df.dropna(inplace=True)
行政_df.dropna(inplace=True)
经济_df.dropna(inplace=True)
政策_df.dropna(inplace=True)
# 1.3转换为列表
教育 = 教育_df.values.tolist()
人物 = 人物_df.values.tolist()
行政 = 行政_df.values.tolist()
经济 = 经济_df.values.tolist()
政策 = 政策_df.values.tolist()


# 2.文本标注
# 2.1文本标注函数
def preprocess_text(content_lines, sentences, category):
    # 定义分词和打标签函数preprocess_text
    # 参数content_lines即为1.3转换的list
    # 参数sentences是定义的空list，用来储存打标签之后的数据
    # 参数category 是类型标签//可以修改成中文、当然数字可能快一点
    for line in content_lines:
        try:
            # 此处line为一个列表，所以转换为string
            segs = jieba.lcut("".join(line))
            segs = [v for v in segs if not str(v).isdigit()]  # 去数字
            segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
            segs = list(filter(lambda x: len(x) > 1, segs))  # 长度为1的字符
            segs = list(
                filter(lambda x: x not in stopwords, segs))  # 去掉停用词
            sentences.append((" ".join(segs), category))  # 打标签
        except Exception:
            print(line)  # 输出错误行、个人认为没用
            continue


# 2.2调用函数、生成训练数据
sentences = []
preprocess_text(教育, sentences, 0)
preprocess_text(人物, sentences, 1)
preprocess_text(行政, sentences, 2)
preprocess_text(经济, sentences, 3)
preprocess_text(政策, sentences, 4)

# 2.3打散数据，生成更可靠的训练集
random.shuffle(sentences)


# 3.模型生成
# 3.1获取所有特征和对应标签
all_texts = [sentence[0] for sentence in sentences]
all_labels = [sentence[1] for sentence in sentences]
# 3.2keras的sequence模块文本序列填充
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_texts)
sequences = tokenizer.texts_to_sequences(all_texts)
word_index = tokenizer.word_index
# print('Found %s unique tokens.' % len(word_index))#小提示//可以看一下
# 下面用到了上面预设的最大长度，可以调大
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
labels = to_categorical(np.asarray(all_labels))
# print('Shape of data tensor:', data.shape)#小提示//可以看一下
# print('Shape of label tensor:', labels.shape)#小提示//可以看一下

# 3.2数据切分//对应前面提到的测试集比例和验证集合比例
p1 = int(len(data) * (1 - VALIDATION_SPLIT - TEST_SPLIT))
p2 = int(len(data) * (1 - TEST_SPLIT))

# 3.3训练集、验证集、测试集生成
# train为训练集
x_train = data[:p1]
y_train = labels[:p1]
# val为验证集
x_val = data[p1:p2]
y_val = labels[p1:p2]
# test为测试集合//按理说可以删掉、我懒
x_test = data[p2:]
y_test = labels[p2:]

# 3.4模型训练//老实说我看不懂
model = Sequential()
model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM,
                    input_length=MAX_SEQUENCE_LENGTH))
model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dense(labels.shape[1], activation='softmax'))
model.summary()

# 3.5模型编译
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])
print(model.metrics_names)
# 下面的参数epochs为训练轮数、越大越好
model.fit(x_train, y_train, validation_data=(
    x_val, y_val), epochs=100, batch_size=128)  # 拟合训练集和验证集、提升准确性

# 3.6保存模型
model.save('训练模型/侨情.侨情')

# 3.7模型评估
print(model.evaluate(x_test, y_test))  # 评估测试集合//其实没有用//仅供娱乐
# 下面这个才是真正的预测函数
# model.predict(经过序列化的数据集合, batch_size=128, verbose=1)
