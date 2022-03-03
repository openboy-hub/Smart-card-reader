from data.model.checkRecordModel import CheckRecordModel
from data.model.employeeDataModel import EmployeeDataModel
from data.model.superUserModel import SuperUserModel
from data.model.workTimeModel import WorkTimeModel
from entity.employee import Employee
from service import hr_service as hr
from entity import organizations as o
from service import recognize_service as rs
import os
import cv2.cv2 as cv2
import numpy as np

PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\data\\"  # 数据文件夹根目录
PIC_PATH = PATH + "faces\\"  # 照片文件夹
# DATA_FILE = PATH + "employee_data.txt"  # 员工信息文件
# WORK_TIME = PATH + "work_time.txt"  # 上下班时间配置文件
# USER_PASSWORD = PATH + "user_password.txt"  # 管理员账号密码文件
# RECORD_FILE = PATH + "lock_record.txt"  # 打卡记录文件

IMG_WIDTH = 640  # 图像的统一宽度
IMG_HEIGHT = 480  # 图像的统一高度


# 自检，检查默认文件缺失
def checking_data_files():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print("数据文件夹丢失，已重新创建：" + PATH)
    if not os.path.exists(PIC_PATH):
        os.mkdir(PIC_PATH)
        print("照片文件夹丢失，已重新创建：" + PIC_PATH)
    print(PIC_PATH)
    sampleDir = PIC_PATH + "1\\"  # 样本1文件路径
    if not os.path.exists(sampleDir):
        os.mkdir(sampleDir)
        sample1 = sampleDir + "1000000000.png"
        sample2 = sampleDir + "2000000000.png"
        sample_img_1 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)  # 创建一个空内容图像
        sample_img_1[:, :, 0] = 255  # 改为纯蓝图像
        cv2.imwrite(sample1, sample_img_1)  # 保存此图像
        print("默认样本1已补充")
        sample_img_2 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)  # 创建一个空内容图像
        sample_img_2[:, :, 1] = 255  # 改为纯蓝图像
        cv2.imwrite(sample2, sample_img_2)  # 保存此图像
        print("默认样本2已补充")
    init_table()


def init_table():
    employeeDataModel = EmployeeDataModel()
    employeeDataModel.createEmpDataTB()
    results = employeeDataModel.selectEmpData()
    if results is not None:
        return
    employeeDataModel.insertEmpDataTB(['ldc', 100000])
    employeeDataModel.closeConnect()
    print("职员信息文件初始化成功")
    checkRecordModel = CheckRecordModel()
    checkRecordModel.createCheckRecordTB()
    checkRecordModel.closeConnect()
    print("打卡记录文件初始化成功")
    superUserModel = SuperUserModel()
    superUserModel.createSuperUserTB()
    superUserModel.insertSuperUserTB([1, 'ldc', '123456'])
    superUserModel.closeConnect()
    print("管理员账号密码文件初始化成功")
    workTimeModel = WorkTimeModel()
    workTimeModel.createWorkTimeTB()
    work_time = workTimeModel.selectWorkTimeById()
    if work_time is not None:
        return
    workTimeModel.insertWorkTimeTB(['08:00:00', '17:00:00'])
    workTimeModel.closeConnect()
    print("上下班时间配置文件初始化成功")


# 加载全部员工信息
def load_employee_info():
    employeeDatasModel = EmployeeDataModel()
    employeeDatas = employeeDatasModel.selectEmpData()
    print(employeeDatas)
    for (id, name, code) in employeeDatas:
        o.add(o.Employee(id, name, code))


# 加载员工图像
def load_employee_pic():
    photos = list()  # 样本图像列表
    lables = list()  # 标签列表
    dirs = os.listdir(PIC_PATH)
    for dir in dirs:
        dirPath = PIC_PATH + dir + "\\"
        pics = os.listdir(dirPath)
        if len(pics) != 0:  # 如果照片文件不是空的
            for file_name in pics:  # 遍历所有图像文件
                print(dirPath + file_name)
                code = file_name[0:o.CODE_LEN]  # 截取文件名开头的特征码
                photos.append(cv2.imread(dirPath + file_name, 0))  # 以灰度图像的方式读取样本
                lables.append(int(code))  # 样本的特征码作为训练标签
        rs.train(photos, lables)  # 识别器训练样本
    else:  # 不存在任何照片
        print("Error >> 员工照片文件丢失，请重新启动程序并录入员工信息！")


# 将员工信息持久化
def save_employee(employee: Employee):
    employeeDataModel = EmployeeDataModel()
    employeeDataModel.insertEmpDataTB([employee.name, employee.code])
    employeeDataModel.closeConnect()


def create_images_dir(id):
    path = PIC_PATH + str(id)
    os.mkdir(path)


# 删除指定员工的所有照片
def remove_pics(id):
    pics = os.listdir(PIC_PATH)  # 读取所有照片文件
    code = str(hr.get_code_with_id(id))  # 获取该员工的特征码
    for file_name in pics:  # 遍历文件
        if file_name.startswith(code):  # 如果文件名以特征码开头
            os.remove(PIC_PATH + file_name)  # 删除此文件
            print("删除照片：" + file_name)


def getEmployeeMaxId():
    employeeDataModel = EmployeeDataModel()
    id = employeeDataModel.selectEmployeeMaxId()
    employeeDataModel.closeConnect()
    return id


def removeEmpById(id):
    employeeDataModel = EmployeeDataModel()
    employeeDataModel.deleteEmpDataTB(id)
    employeeDataModel.closeConnect()


# 加载所有打卡记录
def load_lock_record():
    checkRecordModel = CheckRecordModel()
    results = checkRecordModel.selectCheckRecord()
    records = dict()
    for (id, time, emp_id) in results:
        if emp_id not in records.keys():
            item = list()
            records[emp_id] = item
        records[emp_id].append(time)
    checkRecordModel.closeConnect()
    o.LOCK_RECORD = records  # 将文本转换成打卡记录字典


# 将上下班时间写到文件中
def save_work_time_config(start, end):
    workTimeModel = WorkTimeModel()
    workTimeModel.insertWorkTimeTB([start, end])
    workTimeModel.closeConnect()


# 加载上下班时间数据
def load_work_time_config():
    workTimeModel = WorkTimeModel()
    times = workTimeModel.selectWorkTimeById()
    o.WORK_TIME = times[0]  # 第一个值是上班时间
    o.CLOSING_TIME = times[1]  # 第二个值是下班时间


def save_lock_record(time, employ_id):
    checkRecordModel = CheckRecordModel()
    checkRecordModel.insertCheckRecordTB([time, employ_id])
    checkRecordModel.closeConnect()


# 加载管理员账号密码
def load_users():
    superUserModel = SuperUserModel()
    result = superUserModel.selectSuperUser()
    if len(result) > 0:  # 如果存在文本
        for item in result:
            o.USERS[item[1]] = item[2]
    superUserModel.closeConnect()


# 生成csv文件，采用Windows默认的gbk编码
def create_CSV(file_name, text):
    file = open(PATH + file_name + ".csv", "w", encoding="gbk")  # 打开文件，只写，覆盖
    file.write(text)  # 将文本写入文件中
    file.close()  # 关闭文件
    print("已生成文件，请注意查看：" + PATH + file_name + ".csv")
