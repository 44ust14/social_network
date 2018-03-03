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