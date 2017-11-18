# -*- coding:utf-8 -*-
from schematics.models import Model

from models.base_manager import SNBaseManager
from models.models import UserModel, UserAddModel, UserType
from models.executeSqlite3 import executeSelectOne, executeSelectAll, executeSQL


class UserManager(SNBaseManager):
    user_type = UserType()
    user_type.id = 1
    user_type.type_name = 'test'
    load_models = {}

    def __init__(self):
        self.object = UserModel()

    def getModelFromForm(self,form):
        self.object.first_name = form.get('first_name', '')
        self.object.last_name = form.get('last_name', '')
        self.object.type = self.user_type
        self.object.email = form.get('email', '')
        self.object.nickname = form.get('nickname', '')
        if form.get('passw1', '') == form.get('passw2', ''):
            self.object.password = form.get('passw1', '')
        return self

    def check_user(self):
        self.select().And([('nickname','=',self.object.nickname),('email','=',self.object.email)]).serch()
        print(self.object.id)
        if self.object.id:
            return True
        return False

    def loginUser(self,lofin_form):
        email = lofin_form.get('email', '')
        password = lofin_form.get('passw', '')
        self.select().And([('email','=',email),('password','=',password)]).serch()
        if self.object.id:
            self.load_models[self.object.nickname] = self
            return True
        return False



if __name__ == '__main__':
    manager = UserManager()
    manager.object.id = 1


