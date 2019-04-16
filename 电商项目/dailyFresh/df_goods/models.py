from django.db import models
from tinymce.models import HTMLField   # 富文本编辑器

'''
    分类信息类
'''
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)    # 分类名称
    isDelete = models.BooleanField(default=False)  # 是否删除标志位
    def __str__(self):
        return self.ttitle

'''
    商品信息
'''
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)  # 分类名称
    gpic = models.ImageField(upload_to='df_goods')  # 图片上传路径
    gprice = models.DecimalField(max_digits=5,decimal_places=2)  # 价格
    isDelete = models.BooleanField(default=False)     # 是否删除标志位
    gunit = models.CharField(max_length=20,default='500g')  # 单位
    gclick = models.IntegerField()    # 商品点击量（计算商品人气）
    gjianjie = models.CharField(max_length=200)     # 商品简介
    gkucun = models.IntegerField()          # 库存
    gcontent = HTMLField()                 # 商品详情
    gtype = models.ForeignKey(TypeInfo)   # 关联分类表
    # def __str__(self):
    #     return self.gtitle