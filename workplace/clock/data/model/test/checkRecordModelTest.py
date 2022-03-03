from data.model.checkRecordModel import CheckRecordModel

checkRecordModel = CheckRecordModel()


def insertTest():
    checkRecordModel.insertCheckRecordTB()
    checkRecordModel.closeConnect()


def selectTest1():
    result = checkRecordModel.selectCheckRecord()
    print(result)


def selectTest2():
    result = checkRecordModel.selectCheckRecordByEMPId()
    print(result)


def selectTest3():
    result = checkRecordModel.selectCheckRecordById()
    print(result)


insertTest()
# selectTest1()
# selectTest2()
# selectTest3()
