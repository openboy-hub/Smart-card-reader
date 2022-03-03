import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "face.db")


class CheckRecordModel():
    def __init__(self):
        self.db_path = db_path
        self.conn, self.cur = self.getConnect()

    def getConnect(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        return conn, cur

    def createCheckRecordTB(self):
        create_sql = '''
            create table if not exists check_record(
                record_id integer primary key autoincrement,
                check_time datetime not null default '',
                employee_id integer not null default 0,
                foreign key(employee_id) references employee_data(employee_id)
            )
        '''
        self.cur.execute(create_sql)
        self.conn.commit()

    def insertCheckRecordTB(self, data):
        insert_sql = '''
            insert into check_record(check_time, employee_id)
                values('%s','%s')
        ''' % (data[0], data[1])
        self.cur.execute(insert_sql)
        self.conn.commit()

    def deleteCheckRecordTB(self, id, time):
        delete_sql = '''
            delete from table check_record where employee_id = '%s' and check_time = '%s'
        ''' % (id, time)
        self.cur.execute(delete_sql)
        self.conn.commit()

    def updateCheckRecordTB(self):
        pass

    def selectCheckRecord(self):
        select_sql = '''
            select * from check_record
        '''
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def selectCheckRecordByEMPId(self, id):
        select_sql = '''
            select * from check_record where employee_id = '%s'
        ''' % id
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def selectCheckRecordById(self, id):
        select_sql = '''
            select * from check_record where record_id = '%s'
        ''' % id
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def closeConnect(self):
        self.conn.close()


if __name__ == "__main__":
    checkRecordModel = CheckRecordModel()
    checkRecordModel.createCheckRecordTB()
