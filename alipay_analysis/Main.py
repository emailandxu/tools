from app.fileio.DataReader import DataReader
from app.fileio.DataSaver import DataSaver
from app.sql.alipayOrm import db, Alipay
from app.sql.SQLStatements import SQLStatements
# from ShowTable import ShowTable
import sys

tableHeader = ['tradeId',
               'orderyId',
               'tradeBeginingDate',
               'paidDate',
               'lastModifingDate',
               'tradeSrouce',
               'catagory',
               'tradeCounterPart',
               'prodName',
               'price',
               'io',
               'tradeState',
               'servicePrice',
               'refund',
               'comment',
               'fundState']


def AddCsvToDB():
    # print(DataReader.lines[1])
    # DataSaver.saveTableIntoNewWorkBook(DataReader.lines,tableHeader=tableHeader)
    objs = [Alipay(**dict(zip(tableHeader, tableRow)))
            for tableRow in DataReader.readLines()]
    print('Running db add method')
    db.addAll(objs)
    print('All Done!')

if __name__ == '__main__':
    try:
        queryTemplate = sys.argv[1]
        queryArgs = sys.argv[2:]
        # print(queryTemplate, queryArgs)
    except IndexError as e:
        print("没有提供参数，默认执行数据库更新操作!")
        AddCsvToDB()
        queryTemplate = 'didiEveryDayIncomeInWeek'
        queryArgs = [1,]

    itemsInThisWeek = SQLStatements.get(queryTemplate)(*queryArgs)
    items = itemsInThisWeek.execute().fetchall(withHeader=False)
    import json
    print(json.dumps([[col for col in item] for item in items],ensure_ascii=False,indent=2))
    # print(itemsInThisWeek.getFormatedSQL())
    # print(len(items))
    # print(items)
