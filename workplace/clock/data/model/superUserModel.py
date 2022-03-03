import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "face.db")


class SuperUserModel():
    def __init__(self):
        self.db_path = db_path
        self.conn, self.cur = self.getConnect()

    def getConnect(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        return conn, cur

    def createSuperUserTB(self):
        create_sql = '''
            create table if not exists super_user(
                user_id integer primary key,
                user_name varchar(50) unique not null default '',
                user_password varchar(100) not null default '',
                foreign key(user_id) references employee_data(employee_id) on delete cascade 
            )
        '''
        self.cur.execute(create_sql)
        self.conn.commit()

    def insertSuperUserTB(self, data):
        ids = self.selectSuperUserId()
        ids = [id[0] for id in ids]
        if data[0] in ids:
            return
        insert_sql = '''
            insert into super_user(user_id, user_name, user_password)
                values('%s', '%s', '%s')
        ''' % (data[0], data[1], data[2])
        self.cur.execute(insert_sql)
        self.conn.commit()

    def deleteSuperUserTB(self):
        delete_sql = '''
            delete from table super_user where user_id = '%s'
        ''' % id
        self.cur.execute(delete_sql)
        self.conn.commit()

    def updateSuperUserTB(self):
        pass

    def selectSuperUser(self):
        select_sql = '''
            select * from super_user
        '''
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def selectSuperUserByUserId(self, id=1):
        select_sql = '''
            select * from super_user where user_id = '%s'
        ''' % id
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def selectSuperUserByUserName(self, name):
        select_sql = '''
            select * from super_user where user_name = '%s'
        ''' % name
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def selectSuperUserId(self):
        select_sql = '''
            select user_id from super_user
        '''
        datas = self.cur.execute(select_sql)
        return datas.fetchall()

    def closeConnect(self):
        self.conn.close()


if __name__ == "__main__":
    superUserModel = SuperUserModel()
    print(superUserModel.selectSuperUserId()[0][0])
