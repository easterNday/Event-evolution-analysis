import sqlite3
from 基础函数 import *
from LSTM分类器 import *


# 1.创建SQL数据库
def createSQL(Sqlname='数据库/分类数据库/测试.db'):
     # 1.1创建数据库
    sql = sqlite3.connect(Sqlname)
    # 1.2每个类别生成对应的表
    for typ in TypeTable:
        sql.execute("""
                create table if not exists """ + typ + """(
                id int identity(1,1) primary key,
                link varchar DEFAULT NULL,
                title varchar DEFAULT NULL,
                date varchar DEFAULT NULL,
                writer varchar DEFAULT NULL,
                content varchar DEFAULT NULL)""")
    # 1.3返回对用的sql操作对象
    return sql


# 2.保存SQL数据库
def SaveSQL(Sqlname='数据库/分类数据库/测试.db', tuple=(), typ="测试"):
    # 2.1连接数据库
    sql = sqlite3.connect(Sqlname)
    # 2.2执行对应SQL命令//这里就是获取id,link,title,date,writer,content
    command = "insert into " + typ + \
        " (id,link,title,date,writer,content) values (?,?,?,?,?,?);"
    sql.execute(command, tuple)
    # 2.3通过修改//类似于确认
    sql.commit()


# 3.调用函数
if __name__ == '__main__':
    # 这个叫做测试.db的是我随便起名的，建议正规一点
    createSQL(Sqlname='数据库/分类数据库/测试.db')
    # 3.1打开原始数据库
    initSQL = sqlite3.connect("数据库/原数据库.db")
    # 3.2获取information表格
    cursor = initSQL.execute(
        "SELECT id, link, title, date, writer, content  from information")
    len = 0  # 单纯为了计算操作对象数目
    for row in cursor:
        print("ID = ", row[0])
        print("LINK = ", row[1])
        print("TITLE = ", row[2])
        print("DATE = ", row[3])
        print("WRITER = ", row[4])
        print("CONTENT = ", row[5], "\n")
        len = len + 1  # 单纯为了计算操作对象数目
        # 这里调用保存sql貌似不太合适，可以先把所有数据都存到元组里面后，再循环外面操作，会效果好一点，别问我为什么不写，我懒
        SaveSQL(Sqlname='数据库/分类数据库/测试.db',
                tuple=(row[0], row[1], row[2], row[3], row[4], row[5]), typ=GetType(row[2]))
        # 上面这行的ID可以不写，但同时要修改savesql的代码，因为如果加入id可能导致唯一键报错，或者我们可以使用try来避免这个问题
    # 3.3关闭数据库
    initSQL.close()
