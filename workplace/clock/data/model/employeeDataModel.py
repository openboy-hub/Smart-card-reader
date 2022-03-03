import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "face.db")


class EmployeeDataModel:
    def __init__(self):
        self.db_path = db_path
        self.conn, self.cur = self.getConnect()

    def getConnect(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        return conn, cur

    def createEmpDataTB(self):
        create_sql = '''
            create table if not exists employee_data(
                employee_id integer primary key autoincrement,
                employee_name varchar(10) not null default '',
                employee_individual integer not null default 0
            )
        '''
        self.cur.execute(create_sql)
        self.conn.commit()

    def insertEmpDataTB(self, data):
        insert_sql = '''
            insert into employee_data(employee_name, employee_individual)
                values('%s','%s')
        ''' % (data[0], data[1])
        self.cur.execute(insert_sql)
        self.conn.commit()

    def deleteEmpDataTB(self, id):
        delete_sql = '''
            PRAGMA foreign_keys = ON;
            delete from table employee_data where employee_id = '%s'
        ''' % (id)
        self.cur.execute(delete_sql)
        self.conn.commit()

    def updateEmpDataTB(self):
        pass

    def selectEmpData(self):
        select_sql = '''
            select * from employee_data
        '''
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def selectEmployeeMaxId(self):
        select_sql = '''
            select max(employee_id) from employee_data
        '''
        id = self.cur.execute(select_sql)
        return id.fetchone()[0]

    def closeConnect(self):
        self.conn.close()


if __name__ == '__main__':
    employeeDataModel = EmployeeDataModel()
    employeeDataModel.createEmpDataTB()
    print(employeeDataModel.selectEmployeeMaxId())