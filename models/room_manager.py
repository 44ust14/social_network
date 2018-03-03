# -*- coding:utf-8 -*-
from schematics.models import Model

from models.base_manager import SNBaseManager
from models.models import roomModel, user_room, message
from models.executeSqlite3 import executeSelectOne, executeSelectAll, executeSQL
from models.user_type_manager import UserTypeManager

class RoomManager(SNBaseManager):


    def __init__(self):
        class_model = roomModel
        super(RoomManager, self).__init__(class_model)
    def createRoom(self,user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return
        if self.getFriend(user1, user2):
            return
        self.object.name = 'sdd'
        # self.object.user1 = user1
        # self.object.user2 = user2
        # self.object.block = 2

        return self.save()
    def getFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        self.select().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()
