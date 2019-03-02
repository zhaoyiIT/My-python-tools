'''
 图形界面：
 文件查询：输入文件名，能输出文件路径（支持模糊搜索）
 例：
 输入： 我.jpg
 输出：我们.jpg，我的.jpg，你我.jpg......
'''

import tkinter as tk
import os
import tkinter.messagebox


'''
  创建并设置窗口
'''
window = tk.Tk()
window.title("文件查找")
window.geometry("450x300")

'''
  给窗口加上动态图片
'''
canvas = tk.Canvas(window,height=200,width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(0,0,anchor='nw',image=image_file)
canvas.pack(side='top')

'''
  添加label
'''
tk.Label(window,text='在哪个磁盘下呢：').place(x=50,y=150)
tk.Label(window,text='文件叫什么名字呢：').place(x=50,y=185)

'''
 添加输入框
'''
disk = tk.StringVar()
entry_usr_name = tk.Entry(window,textvariable=disk)
entry_usr_name.place(x=160,y=150)

file = tk.StringVar()
entry_usr_name = tk.Entry(window,textvariable=file)
entry_usr_name.place(x=160,y=185)

'''
    2个弹框函数
'''
    # 找到文件
def get_result_succeed(file_path):
    tkinter.messagebox.showinfo('查询结果', file_path)

def get_result_faied():
    tkinter.messagebox.showwarning('警告', '很遗憾，没有找到文件位置')

flag = False
final_path = ""
def query_file_path():
    # 获取输入的盘符与文件名
    disk_name = disk.get()
    file_name = file.get()
    disk_name += ':\\'
    # 创建队列
    file_list = []
    # 将第一个目录加入队列
    file_list.append(disk_name)

    while len(file_list) > 0:
        path = file_list.pop(0)
        if os.path.isdir(path):
            allFile = os.listdir(path)
            for el in allFile:
                newPath = os.path.join(path,el)
                file_list.append(newPath)
        else:
            # 获取path最后的文件名
            target = os.path.basename(path)
            if target.split('.')[0] == file_name:
                get_result_succeed(path)
                return 1
    get_result_faied()
    return 1

'''
    查询按钮
'''

btn_login = tk.Button(window,text='查询',command=query_file_path)
btn_login.place(x=170,y=230)


# 启动窗口
window.mainloop()




