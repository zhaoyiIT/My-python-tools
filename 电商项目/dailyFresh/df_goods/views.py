from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponse
from df_goods.models import *
'''
    首页展示逻辑
'''
def index(request):
    # 查询各分类的最新4条、最热4条数据
    typelist = TypeInfo.objects.all()        #首先获得外键指向的表中对象，然后通过‘_set’这样的方法获得目标表中的数据
    # 获得海鲜类：最新2条
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:2]          #按降序获得,获得最大的
    # 获得海鲜类：最热2条
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:2]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:2]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:2]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:2]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:2]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:2]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:2]
    context = {
        'title':'首页',
        'type0':type0, 'type01':type01,
        'type1':type1, 'type11':type11,
        'type2':type2, 'type21':type21,
        'type3':type3, 'type31':type31,
    }

    return render(request, 'df_goods/index1.html', context)

'''
    列表页
'''

def list(request, tid, pindex, sort):  #列表页     #分别为类型的id,第几页,按什么排序
    typeinfo = TypeInfo.objects.get(id=int(tid))    # 得到一个分类
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]  #取该类型最新的两个
    if sort == '1':   #默认  最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        # print(22233)
    elif sort == '2':     #按价格排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list,10)         #分页, 每页有几个元素
    page = paginator.page(int(pindex))          #获得pindex页的元素列表
    context = {
        'title':typeinfo.ttitle,    #类型名称  为了给base传递title
        'page':page,        #排序后的每页的元素列表
        'typeinfo':typeinfo,    #类型信息
        'news':news,    #新品推荐列表
        'sort':sort,    #传递排序数字, 方便图标active
        'paginator':paginator,  #分页
    }
    return render(request, 'df_goods/list1.html', context)
