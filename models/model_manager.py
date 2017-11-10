# -*- coding:utf-8 -*-
from schematics.models import Model
from models.models import UserModel, UserAddModel, UserType
from models.executeSqlite3 import executeSelectOne, executeSelectAll, executeSQL


class UserManager():
    user_type = UserType()
    user_type.id = 1
    user_type.id = 'user'
    load_models = {}

    def __init__(self):
        self.user = UserModel()

    def getModelFromForm(self,form):
        self.user.first_name = form.get('first_name', '')
        self.user.last_name = form.get('last_name', '')
        self.user.type = self.user_type
        self.user.email = form.get('email', '')
        self.user.nickname = form.get('nickname', '')
        if form.get('passw1', '') == form.get('passw2', ''):
            self.user.password = form.get('passw1', '')
        return self

    def check_user(self):
        sql = 'SELECT * FROM users WHERE nickname = "{}" or email = "{}"'.format(self.user.nickname, self.user.email)
        check_user = executeSelectOne(sql)
        if check_user:
            return True
        return False


    def addNewUser(self):
        sql = 'INSERT INTO users (first_name, last_name, type, email, nickname, password, create_time) VALUES ("{}","{}","{}","{}","{}","{}","{}")' \
            .format(self.user.first_name, self.user.last_name, self.user_type,
                    self.user.email, self.user.nickname, self.user.password, self.user.create_time)
        return executeSQL(sql)

    def selectUser(self,data=[]):
        self.user.id = data[0]
        self.user.first_name = data[1]
        self.user.last_name = data[2]
        self.user.type = self.user_type
        self.user.email = data[7]
        self.user.nickname = data[8]
        self.user.password = data[9]
        self.user.create_time = data[10]
        self._selectUserAdd()


    def _selectUserAdd(self):
        sql = 'SELECT * FROM users_add WHERE user = {}'.format(self.user.id)
        user_add = UserAddModel()
        user_add_data = executeSelectOne(sql)
        if not user_add_data:
            return user_add
        user_add_data = user_add_data[0]
        self.user.user_add_data.age = user_add[1]
        self.user.user_add_data.create_time = user_add[2]
        self.user.user_add_data.phone = user_add[3]
        self.user.user_add_data.address = user_add[4]
        self.user.user_add_data.sex = user_add[5]



    def loginUser(self,lofin_form):
        email = lofin_form.get('email', '')
        password = lofin_form.get('passw', '')
        sql = 'select * from users where email = "{}" and password = "{}"'.format(email, password)
        user = executeSelectOne(sql)
        # print(user)
        if user:
            self.selectUser(user)
            self.load_models[self.user.nickname] = self.user
            # print(self.user)
            return True
        return False

    def toDict(self):
        def recurs(model):
            result = {}
            items = model.items()
            for it in items:
                if isinstance(it[1], Model):
                    result[it[0]] = recurs(it[1])
                result[it[0]] = it[1]
            return result
        return recurs(self.user)


if __name__ == '__main__':
    manager = UserManager()
    manager.user.id = 1
    manager.selectUser()
    print(manager.toDict())


