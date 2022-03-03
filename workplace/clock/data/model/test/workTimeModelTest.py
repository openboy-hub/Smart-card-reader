from data.model.workTimeModel import WorkTimeModel

workTimeModel = WorkTimeModel()


def insertTest():
    workTimeModel.insertWorkTimeTB()
    workTimeModel.closeConnect()


def selectTest():
    workTimeModel.selectWorkTimeById()
    workTimeModel.closeConnect()
