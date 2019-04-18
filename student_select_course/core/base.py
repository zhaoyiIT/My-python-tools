'''
   本文件放父类
'''
from conf.settings import course_info
import pickle


class Base:
    def __str__(self):
        return self.name


class Person:

    def show_courses(self):  #  查看所有课程
        for count,course in enumerate(self.get_from_pickle(course_info),1):
            print(count, course)

     # 从student_info,course_info 获得对象  (本方法涉及了所有的读文件操作)
    @staticmethod
    def get_from_pickle(path):
        with open(path,'rb') as f:
            while 1:
                try:
                    stu_obj = pickle.load(f)
                    yield stu_obj
                except EOFError:
                    break

    def dump_obj(self,path,obj):
        with open(path,mode='ab') as f:        # 'ab'模式表示 以二进制形式往文件中追加
            pickle.dump(obj,f)