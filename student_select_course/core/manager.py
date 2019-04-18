from core.base import Person
from core.course import *
from core.student import *
from conf.settings import *

class Manager(Person):
    operate_lst = [('创建课程','create_course'),
                   ('创建学生','create_student'),
                   ('查看所有课程','show_courses'),
                   ('查看所有学生','show_students'),
                   ('查看所有学生的选课情况','show_student_course'),
                   ('退出','exit')]
    def __init__(self,name):
        self.name = name

    def create_course(self):   # 创建课程
        name = input('课程名称：')
        price = input('课程价格')
        period = input('课程周期')
        teacher = input('课程讲师')
        course_obj = Courses(name,price,period,teacher)     # 创建一个课程对象

        self.dump_obj(course_info,course_obj)

        print('%s课程创建成功' % course_obj.name)

    def create_student(self):   # 创建学生
        # 创建学生有2个工作要做：1 将用户名和密码写入到userinfo; 2 将学生对象存到student_info 文件
        stu_name = input('学生账号：')
        stu_pwd = input('学生密码：')
        stu_obj = Student(stu_name)
        stu_auth = '%s|%s|Student\n' % (stu_name,stu_pwd)
        with open(userinfo,mode='a',encoding='utf-8') as f:
            f.write(stu_auth)
        self.dump_obj(student_info,stu_obj)


        print('%s学生创建成功' % stu_obj.name)

    def show_students(self):   # 查看所有学生
        for count,stu in enumerate(self.get_from_pickle(student_info),1):
            print(count,stu)   # 调用对象的__str__方法

    def show_student_course(self):             #  查看学生已选课程
        for stu in self.get_from_pickle(student_info):
            print(stu)   # 打印对象，将会自动调用学生对象的__str__方法,__str__如果没有的话，就会找__repr__方法

    def exit(self):
        exit()

    @classmethod
    def init(cls,name):
        # 返回管理员对象
        return cls(name)