from keras.models import load_model
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import numpy as np

# 1.获取停词表
from 基础函数 import *
stopwords = getStopWords()


# 2.获取文本类型的函数
def GetType(input="华侨华人蓝皮书"):

    tokenizer = Tokenizer()
    # 2.1加载模型
    model = load_model('训练模型/侨情.侨情')
    # 以下的命名我随意命名的、大家看看就好
    # 2.2定义空列表存放用于获取类型的输入单元
    just4test = []
    # 2.3打包成相关的data（就是我在LSTM生成的时候提到的序列化东东）
    just4test.append(Just_text(input))
    tokenizer.fit_on_texts(just4test)
    just1sequences = tokenizer.texts_to_sequences(just4test)
    just1data = pad_sequences(just1sequences, maxlen=MAX_SEQUENCE_LENGTH)
    just1labels = to_categorical(np.asarray([0, 0]))
    just1x_test = just1data
    # 2.4预测类型、相似度比较（我在LSTM生成里面也说到了、就在最后一行）
    y_predict = model.predict(just1x_test, batch_size=128, verbose=1)
    # 2.5获取类别的索引
    maxindex = np.argmax(y_predict)
    # 2.6返回相应类别
    return TypeTable[maxindex]
