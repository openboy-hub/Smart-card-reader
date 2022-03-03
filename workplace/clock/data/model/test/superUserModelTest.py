from data.model.superUserModel import SuperUserModel

superUserModel = SuperUserModel()


def insertTest():
    superUserModel.insertSuperUserTB()
    superUserModel.closeConnect()


def selectTest1():
    result = superUserModel.selectSuperUser()
    print(result)


def selectTest2():
    result = superUserModel.selectSuperUserByUserId()
    print(result)


def selectTest3():
    result = superUserModel.selectSuperUserByUserName()
    print(result)


insertTest()
# selectTest1()
# selectTest2()
# selectTest3()
