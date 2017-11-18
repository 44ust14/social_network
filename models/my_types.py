# -*- coding:utf-8 -*-
from schematics.types import BaseType ,ModelType
from schematics.exceptions import ValidationError
from schematics.models import Model

class One2One(ModelType):
    pass


if __name__ == '__main__':

    class Test(Model):
        test = One2One()

    test = Test()
    test.test= 10

    print(test)



