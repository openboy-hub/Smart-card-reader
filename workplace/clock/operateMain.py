"""
主入口
"""
import datetime


from util import camera
from service import hr_service as hr
from util import public_tools as tool
from entity import organizations as o

from util import io_tools as io


def login(username, password):
    if hr.valid_user(username.strip(), password.strip()):  # 校验账号密码
        return True
    else:
        return False


# 员工管理
def registerImage():
    id = o.get_new_id()
    io.create_images_dir(id)
    code = tool.randomCode()  # 生成随机特征码
    status = camera.register(code, id)  # 打开摄像头为员工照相
    return status, code


def registerEmployee(name, code):
    hr.add_new_employee(name, code)  # 人事服务添加新员工，并获得该员工的特征码


def deleteEmployee(id):
    hr.remove_employee(id)  # 人事服务删除该员工


def check_record(someday=datetime.datetime.now().strftime('%Y-%m-%d')):
    hr.get_record_today(someday)


# 查看记录
def check_employee_list():
    hr.get_employee_report()


# 报表设置
def report_config(work_start, work_end):
    work_start = tool.timeutc(work_start)
    work_end = tool.timeutc(work_end)
    hr.save_work_time(work_start, work_end)  # 保存用户设置的上班时间和下班时间


# 考勤报表
def check_day_report(date='today'):
    if date == "today":
        hr.get_today_report()  # 打印今天的日报
    else:
        hr.get_day_report(date)  # 打印指定日期的日报


def check_month_report(month='premonth'):
    if month == 'premonth':
        hr.get_pre_month_report()  # 生成上个月的月报
    else:
        hr.get_month_report(month)  # 生成指定月份的月报


# 人脸打卡
def face_clock():
    camera.clock_in()
