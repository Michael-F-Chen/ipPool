import datetime
import urllib
from lxml import etree

def xiciHandle(self, content):
    xici_ips = set()

    et = etree.HTML(content)
    result_even = et.xpath('//tr[@class=""]')
    result_odd = et.xpath('//tr[@class="odd"]')
    # 因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
    # 刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
    # 使用上面的方法可以不管网页怎么改，都可以抓到ip 和port

    for i in result_even:
        t1 = i.xpath("./td/text()")[:2]  # 获得 ip 和 端口
        proxy = {'http': 'http://' + t1[0] + ':' + t1[1]}  # 拼接 地址
        print("IP:%s\tPort:%s" % (t1[0], t1[1]))
        xici_ips.add(t1[0] + ':' + t1[1])
    for i in result_odd:
        t2 = i.xpath("./td/text()")[:2]  # 获得 ip 和 端口
        proxy = {'http': 'http://' + t2[0] + ':' + t2[1]}  # 拼接 地址
        print("IP:%s\tPort:%s" % (t2[0], t2[1]))
        xici_ips.add(t2[0] + ':' + t2[1])

    return xici_ips