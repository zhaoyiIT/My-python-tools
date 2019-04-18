import os

base = os.path.dirname(os.path.dirname(__file__))   #  __file__  指的是当前py文件
db = os.path.join(base,'db')

'''
    拼接获取到3个文件的路径
'''
course_info = os.path.join(db,'course_info')
student_info =os.path.join(db, 'student_info')
userinfo =os.path.join(db, 'userinfo')

