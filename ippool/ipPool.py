import datetime
import urllib
from ippool.websHandle import xiciHandle


class ipPool():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header = {"User-Agent": self.user_agent}
        self.now = datetime.time.strftime("%Y-%m-%d")

    #爬取各种代理ip
    def getIps(self):
        xici = 'http://www.xicidaili.com/nn/'  # 代理目标网址
        kuaidaili = ''

        ipsNoCheck = set()
        ipsChecked = set()

        nn_url = (xici, kuaidaili)  # 网址list

        for url in nn_url:
            req = urllib.request.Request(url, headers=self.header)  # 提交请求

            resp = urllib.request.urlopen(req, timeout=10)  # 获得response
            # 此处可能会出现异常

            content = resp.read()

            if url == xici:  # 逐个处理
                ipsNoCheck.add(xiciHandle(content))
            else:
                pass

        for proxy in ipsNoCheck:
            if self.isAlive(proxy):  # 逐个验证是否可用
                ipsChecked.add(proxy)  # 可用的网址调出

        return ipsChecked

    #验证ip是否可用
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
    obj=ipPool()
    obj.loop(2)
    end = datetime.datetime.now()
    print("end at %s" % end)





