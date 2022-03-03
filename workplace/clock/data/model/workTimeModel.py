import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "face.db")


class WorkTimeModel():
    def __init__(self):
        self.db_path = db_path
        self.conn, self.cur = self.getConnect()

    def getConnect(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        return conn, cur

    def createWorkTimeTB(self):
        create_sql = '''
            create table if not exists work_time(
                time_id integer primary key autoincrement,
                start time not null default '',
                end time not null default ''
            )
        '''
        self.cur.execute(create_sql)
        self.conn.commit()

    def insertWorkTimeTB(self, data):
        insert_sql = '''
            insert into work_time(start, end)
                values('%s','%s')
        ''' % (data[0], data[1])
        self.cur.execute(insert_sql)
        self.conn.commit()

    def deleteWorkTimeTB(self, id):
        delete_sql = '''
            delete from table work_time where time_id = '%s'
        ''' % id
        self.cur.execute(delete_sql)
        self.conn.commit()

    def updateWorkTimeTB(self):
        pass

    def selectWorkTimeById(self, id=1):
        select_sql = '''
            select * from work_time where time_id = '%s'
        ''' % id
        datas = self.cur.execute(select_sql)
        return datas.fetchall()[0]

    def closeConnect(self):
        self.conn.close()


if __name__ == "__main__":
    workTimeModel = WorkTimeModel()
    print(workTimeModel.selectWorkTimeById())
