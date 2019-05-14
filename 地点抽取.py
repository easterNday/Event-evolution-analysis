import cpca
import jieba.posseg as pseg
import pandas as pd
import xlsxwriter

location_str = ["北京","观山湖区"]
df = cpca.transform(location_str, cut=False, pos_sensitive=True)
print(df)

# 主函数
if __name__ == '__main__':
    # 1.输入文件
    data_xls = pd.read_excel('词云/法国新闻.xlsx')

    # 2.这种方法是因为我用直接读取的方法有点麻烦
    test_data = []
    for i in data_xls.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = data_xls.loc[i, ['链接','新闻', '日期','来源', '内容']].to_dict()
        test_data.append(row_data)
    print("最终获取到的数据是：{0}".format(test_data))

    #3.抽取内容中的地名和机构名
    for i in test_data:
        words = pseg.cut(i["内容"])
        i["地点"] = ""
        for word, flag in words:
            if (flag == 'ns'or flag == "nt"):
                print('%s, %s' % (word, flag))
                i["地点"] += word + "\n"

    #4.保存抽取出来的地点
    # 创建工作簿
    file_name = "涉侨资讯_慈善公益.xlsx"
    workbook = xlsxwriter.Workbook(file_name)
    # 创建工作表
    worksheet = workbook.add_worksheet('慈善公益')
    # 写单元格
    worksheet.write(0, 0, '链接')
    worksheet.write(0, 1, '新闻')
    worksheet.write(0, 2, '日期')
    worksheet.write(0, 3, '来源')
    worksheet.write(0, 4, '地点')
    worksheet.write(0, 5, '内容')

    pla = 1
    for i in test_data:
        print(i)
        worksheet.write_row(pla, 0, (i['链接'],i['新闻'],i['日期'],i['来源'],i["地点"],i['内容']))
        pla = pla+1

    # 关闭工作簿
    workbook.close()
