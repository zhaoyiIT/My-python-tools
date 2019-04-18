import sys,os
import pickle
from conf.settings import *
from core.auth import login
from core.manager import Manager
from core.course import Courses
from core.student import Student
#这句代码的意思是反射到当前py文件，<module '__main__' from 'G:/每周作业/Eva_J  校园管理系统/01/version 1.py'>
#  print(sys.modules[__name__])


def main():
    ret = login()
    if ret['result']:   # 如果用户登录成功，就展示用户选项，让用户输入序号去选择
        print('\033[1;32;40m登录成功！\033[0m')  # 带背景色输出
        if hasattr(sys.modules[__name__],ret['id']):  # 反射：检测是否存在这个类
            cls = getattr(sys.modules[__name__],ret['id'])  # 反射：得到这个类
            # obj = cls(ret['name'])
            obj = cls.init(ret['name'])
            for id,(item,_) in enumerate(cls.operate_lst,1):
                print(id,item)
            while 1:
                # 获取用户输入的数字，对应的函数名称
                func_str = cls.operate_lst[int(input('请输入选项：'))-1][1]
                if hasattr(obj,func_str):
                    getattr(obj,func_str)()