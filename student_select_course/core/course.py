from core.base import *

class Courses(Base):
    def __init__(self,name,price,period,teacher):
        self.name = name
        self.price = price
        self.period = period
        self.teacher = teacher



    def __str__(self):
        return ' '.join([self.name, self.price, self.period, self.teacher])