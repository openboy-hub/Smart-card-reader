from data.model.employeeDataModel import EmployeeDataModel

employeeDataModel = EmployeeDataModel()


def insertTest():
    with open("../../employee_data.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            id, name, code = line.split(',')
            print(id, name, code)
            employeeDataModel.insertEmpDataTB([id, name, code])
    employeeDataModel.closeConnect()


def selectTest():
    result = employeeDataModel.selectEmpData()
    print(result)


insertTest()
# selectTest()
