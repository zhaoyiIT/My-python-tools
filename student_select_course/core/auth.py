from conf.settings import userinfo

# 登录，可以自动识别身份
# 用户名|密码|身份
def login():
    uname = input('用户名:')
    pwd = input('密码：')
    with open(userinfo,mode='r',encoding='utf-8') as f:
        for line in f:
            user_name,password,identify = line.strip().split('|')
            if uname == user_name and pwd == password:
                return {'result':True,'name':user_name,'id':identify}
        else:
            return {'result':False,'name':uname}