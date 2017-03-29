
import urllib, datetime
import time

from lxml import etree

"""
    date:2017年3月8日
    IDE :Pycharm
    author: ChenFei
    version:Python3.4
    aim:    通过爬取免费ip代理网站，获取大量代理IP，并测试获得可用IP
"""
#获得代理
class getProxy():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header = {"User-Agent": self.user_agent}
        self.now = time.strftime("%Y-%m-%d")

    def getContent(self, num):

        nn_url = "http://www.xicidaili.com/nn/"                             #目标网站
        req = urllib.request.Request(nn_url, headers=self.header)           #提交请求

        resp = urllib.request.urlopen(req, timeout=10)                      #获得response
        #此处可能会出现异常

        content = resp.read()                                               #读取response

        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')
        #因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
        #刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
        #使用上面的方法可以不管网页怎么改，都可以抓到ip 和port

        for i in result_even:
            t1 = i.xpath("./td/text()")[:2]                                 #获得 ip 和 端口
            proxy = {'http': 'http://' + t1[0] + ':' + t1[1]}               #拼接 地址
            print ("IP:%s\tPort:%s" % (t1[0], t1[1]))
            if self.isAlive(proxy):                                          #判断是否可用
                self.insert_file(self.now,t1[0],t1[1])                          #写入文本
        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]                                 #获得 ip 和 端口
            proxy = {'http': 'http://' + t2[0] + ':' + t2[1]}               #拼接 地址
            print ("IP:%s\tPort:%s" % (t2[0], t2[1]))
            if self.isAlive(proxy):                                         #判断是否可用
                self.insert_file(self.now,t2[0],t2[1])                          #写入文本

    #将可用的代理写入指定文本
    def insert_file(self,date,ip,port):
        with open("%s.txt"%date,'a+') as f:
            f.write(ip + ":" + port +"""\r""")

    #翻页
    def loop(self,page=5):
        for i in range(1,page):
            self.getContent(i)

    #查看爬到的代理IP是否可用
    def isAlive(self,proxy):
        #http: // icanhazip.com /
        print (proxy)

        #使用这个方式是全局方法。
        proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        #使用代理访问百度官网，进行验证代理是否有效
        test_url="http://www.baidu.com"
        req = urllib.request.Request(test_url,headers=self.header)
        try:
            #timeout 设置为10，如果你不能忍受你的代理延时超过10，就修改timeout的数字
            resp=urllib.request.urlopen(req,timeout=5)#timeout=1000
            #a = resp.read().decode('utf-8')
            #print(a)
            if resp.code==200:
                print ("work")
                return True
            else:
                print ("not work")
                return False
        except :
            print ("Not work")
            return False

if __name__ == "__main__":
    now = datetime.datetime.now()
    print ("Start at %s" % now)
    obj=getProxy()
    obj.loop(2)
    end = datetime.datetime.now()
    print("end at %s" % end)
