import os
from conf.settings import student_info
from core.base import *

class Student(Person,Base):
    operate_lst = [('查看可选课程','show_courses'),
                   ('选择课程','selece_course'),
                   ('查看所选课程','check_selected_course'),
                   ('退出课程','exit')
                   ]
    def __init__(self,name):
        self.name = name
        self.courses = []

    def __repr__(self):
        course = [course.name for course in self.courses]  # 得到课程名称列表
        return '%s %s' %(self.name, '所选课程：%s' % ('|').join(course))


    def selece_course(self):     # 学生选择课程
        self.show_courses()   # 展示课程
        num = int(input('输入你要选择的课程编号：'))

        for count,couse in enumerate(self.get_from_pickle(course_info),1):
            if num == count:
                self.courses.append(couse)  # 加入到选课列表
                print('你选择的课程是%s' % couse)   # 打印课程对象，自动调用__str__方法
                break
        else:
            print('没有你要找的课程')

    def check_selected_course(self):
        print('查看所选课程')
        for course in self.courses:
            print(course.name,course.teacher)

    def exit(self):         # 退出，退出的时候要将修改了的学生信息（给学生添加了课程列表），写到新文件中，并且将原文件改名
        with open(student_info+'_bak',mode='wb') as f2:
            for stu in self.get_from_pickle(student_info):
                if stu.name == self.name:  # 如果判断是当前学生对象的话（即：已经修改了的学生）
                    pickle.dump(self, f2)  # 将当前对象写回到f2
                else:
                    pickle.dump(stu, f2)
        os.remove(student_info)
        os.rename(student_info+'_bak',student_info)
        exit()



    # @classmethod,因为cls没有用到，所以可以使用staticmethod代替
    @classmethod
    def init(cls,name):
        # 返回一个学生对象，在文件里
        # 找到符合的对象后，直接返回这个对象

        for stu in cls.get_from_pickle(student_info):
            if stu.name == name:
                return stu
        else:
            print('没有这个学生')