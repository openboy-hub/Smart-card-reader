"""
组织结构
"""
from entity.employee import Employee
from util import io_tools as io

LOCK_RECORD = dict()  # 打卡记录字典，格式为{员工id：[时间1，时间2]}
EMPLOYEES = list()  # 全体员工列表
CODE_LEN = 6  # 特征码的默认长度
WORK_TIME = ""  # 上班时间
CLOSING_TIME = ""  # 工下班时间
USERS = dict()  # 管理员账号密码


# 添加新员工
def add(e: Employee):
    EMPLOYEES.append(e)


# 删除指定ID的员工记录
def remove(id):
    io.removeEmpById(id)


# 获取新员工的ID
def get_new_id():
    return io.getEmployeeMaxId()+1
