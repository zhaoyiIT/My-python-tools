#coding = utf-8
from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)   # 用户名
    upwd = models.CharField(max_length=40)      # 密码
    uemail = models.CharField(max_length=30)    # 邮箱
    ushou = models.CharField(max_length=20,default='')     # 收件人
    uaddress = models.CharField(max_length=100,default='')     # 收件地址
    uyoubian = models.CharField(max_length=6,default='')       # 邮编
    uphone = models.CharField(max_length=11,default='')        # 手机号
