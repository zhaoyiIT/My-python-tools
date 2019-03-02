import random
from time import sleep

money = int(input('>>>红包金额:'))
count = int(input('>>>红包个数：'))

# 根据人数建立列表
person  = []
a = 1
while a < count+1:
    person.append('第'+str(a)+'个人')
    a += 1

# 所有涉及金额的浮点数都需要用 round 方法保留2位小数
money  =round(float(money),2)
# 字典：最后可以计算手气最佳
redPacket_dic = {}
i = 0 # 表示发到第几次红包了
while count:
    count -= 1
    if count == 0:
        print('%s抢到红包%s元，红包抢完了！'%(person[i],money))
        redPacket_dic[money] = person[i]
    elif count > 0:
        # 红包算法：在0.01到红包总金额之间取随机数/红包剩余个数
        red_packet = round(random.uniform(0.01,money)/count,2)
        redPacket_dic[red_packet] = person[i]
        print('%s抢到红包%s元，剩余%s个！'%(person[i],red_packet,count))
        # 计算余额
        money = round((money - red_packet),2)
        i += 1
    sleep(1)

# 输出运气最佳
best = max(redPacket_dic.items())
print('%s运气最佳，抢到了%s元' %(best[1],best[0]))