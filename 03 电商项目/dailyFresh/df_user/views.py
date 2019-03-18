from django.http import JsonResponse
from hashlib import md5
from django.shortcuts import render,redirect,HttpResponseRedirect
from df_user.models import *
# Create your views here.

'''
    跳转到注册页面
'''
def register(request):
    return render(request,'df_user/register.html')

'''
    接收用户注册信息并保存到db
'''
def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断2次输入密码
    if upwd != upwd2:
        return redirect('/user/register')
    # 对密码加密
    hash_obj = md5(b'passwordsecret')
    hash_obj.update(upwd.encode('utf-8'))
    upwd_secret = hash_obj.hexdigest()

    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_secret
    user.uemail = uemail
    user.save()  # 保存到数据库

    # 注册完成了，跳转到页面
    return redirect('/user/login')

'''
    判断用户名是否存在
'''
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})  # 自动转json格式

'''
  跳转到登录页面
'''
def login(request):
    uname = request.COOKIES.get('uname','')  # 从cookie中取出登录的用户名
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

'''
    用户登录方法
'''
def login_handle(request):

    # 获取用户输入信息
    post = request.POST   # 返回一个字典
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)  # 获取用户是否勾选了‘记住用户名’

    # 根据用户名查询对象是否存在
    users = UserInfo.objects.filter(uname=uname)  # 返回一个列表
    print('users:',users)
    # 判断用户名如果存在
    if len(users) == 1:
        hashObj = md5(b'passwordsecret')
        hashObj.update(upwd.encode('utf-8'))
        # 如果密码输入正确
        if hashObj.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info') # 验证成功后，去用户中心页面
            # 根据勾选状态，写入cookie
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1) # 设置cookie时间：立即过期
            request.session['user_id'] = users[0].id     # 记录session的作用：在访问登录以后的页面时，能用到
            request.session['user_name'] = uname
            return red
        # 如果密码输入错误
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    # 如果用户名不存在
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

'''
    跳转到用户中心界面
'''
def toUserInfo(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail    # 对象.属性
    context = {
        'title':'用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name']
    }
    return render(request,'df_user/user_center_info.html',context)


'''
    跳转到用户中心->全部订单页面
'''
def turnToOrder(request):
    context = {'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)


'''
    跳转到用户中心->收货地址页面
'''
def turnToSite(request):
    '''
        编辑收货地址逻辑
    '''
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)