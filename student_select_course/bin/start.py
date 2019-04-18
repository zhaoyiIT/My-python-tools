import os,sys
# print(os.path.dirname(__file__))  # G:/每周作业/student_select_course/bin

# 将项目路径添加到Python解释器的模块搜索路径
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from core.core import *

if __name__ == '__main__':
    main()