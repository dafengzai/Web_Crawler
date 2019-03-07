# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import json
import time
import random

class SpiderFrameSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        
        
test_i = 0
        
class ChangeProxy(object):
    '''
    当本地IP失效时，开始使用代理IP，代理IP失败2次后取消代理IP。
    解决
    1.切换IP时机
        判断IP是否失效
        IP确认是否可用
            在第一次使用与使用10次后确认下IP是否可用
    2.如何切换
        我买的这个获取间隔至少是10秒
        一次请求几个？
        一个代理IP用几次后清除
    '''
    
    def __init__(self):
        self.get_url = "http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=17083e63ce6a4e6192e97389ee8d2b2b&count=5&expiryDate=0&format=1&newLine=2"
        #self.get_url = "http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=6ad0b7ed0f4045a6a7df4b563b9353c0&count=5&expiryDate=0&format=1&newLine=2"
        self.test_url = "http://guba.eastmoney.com/list,601398_1.html"
        self.ip_list = [] #我每次抓10个IP
        self.count = 0 #第几次调用
        self.ip_num = 0 #正在使用第几个IP
        self.ip_fall_count = [0 for i in range(5)] #记录每个IP使用次数，初始皆为0
        #
        self.ip_used_times = [0 for i in range(5)]
        self.test_i = 0
        
        self.start_time = 0;
        
    def get_ip_data(self):  
        self.test_i = self.test_i+1
        print("test_2:get_ip activate")
        print(self.test_i)
        tem_response = requests.get(self.get_url)
        tem_data = json.loads(tem_response.text)
        
        while(int(tem_data['code']) != 0) : #提取错误，一般是太频繁
            time.sleep(5.5)
            tem_response = requests.get(self.get_url)
            tem_data = json.loads(tem_response.text)
            
        self.ip_list.clear() #清空IP池
        for ele in tem_data['msg']:
            self.ip_list.append({"ip":ele['ip'], "port":ele['port']})
            
        self.ip_fall_count = [0 for i in range(5)]
        self.ip_num = 0
        self.ip_used_times = [0 for i in range(5)]
        
        self.start_time = time.time()
        
    def if_ip_used(self):
        curr_proxy = "http://"+self.ip_list[self.ip_num]["ip"]+":"+self.ip_list[self.ip_num]["port"]
        print(curr_proxy)
        try:
            test_req = requests.get(url = self.test_url, proxies = {'http':curr_proxy},timeout=2)
            if test_req.status_code == 200: #ip可用
                return True
        except:
            return False
        return False
        #pass
    
    def check_ip(self):
        #now_time = time.time()
        #if int(now_time-self.start_time) >= 40:
        #    self.get_ip_data()
        self.ip_num = (self.ip_num+1)%5 #轮流使用
        
        if self.ip_used_times[self.ip_num] >= 16:
            self.ip_fall_count[self.ip_num] = self.ip_fall_count[self.ip_num]+1
        
        flag = 0
        for i in range(self.ip_num, self.ip_num+4): #本次代理已失效，换下一个代理
            if self.ip_fall_count[i%5] < 1: #有效2
                self.ip_num = i%5
                flag = 1
                break
        if flag == 0:
            print("haha")
            #全部失效
            self.get_ip_data()
            print("ip_pool is changing")
        
        #第一次
            
        
        #while(self.ip_used_times[self.ip_num]==0 or self.ip_used_times[self.ip_num]==1): #2说不定更好
        while(1):
            
            print("hehe")

            if self.if_ip_used() == True: #IP可用
                print("ip_usefull")
                #if self.ip_used_times[self.ip_num]==2:
                #    self.ip_used_times[self.ip_num]=0
                return
            
            self.ip_fall_count[self.ip_num] = self.ip_fall_count[self.ip_num]+1
            flag = 0
            for i in range(self.ip_num+1, self.ip_num+5): #本次代理已失效，换下一个代理
                if self.ip_fall_count[i%5] < 1: #失效2次内
                    self.ip_num = i%5
                    flag = 1
                    break
            if flag == 1:
                break
            
            print(self.ip_fall_count)
            print("haha")
            #全部失效
            self.get_ip_data()
            print("ip_pool is changing")
            
            
          
            
    def process_request(self, request, spider):
        #大概使用几十次的时候，确认下IP是否可用
        
        if self.count == 0: #初始化值为0，即第一次使用，不需要变IP
            self.get_ip_data()
            self.count = self.count+1
            return None
         
        #return None
    
        #print("test_4")
        self.check_ip()
        proxy = "http://"+self.ip_list[self.ip_num]["ip"]+":"+self.ip_list[self.ip_num]["port"]
        self.ip_used_times[self.ip_num] = self.ip_used_times[self.ip_num]+1
        print("proxy is changing")  
        # 对当前reque加上代理  
        request.meta['proxy'] = proxy 
        
   
class Random_Useragent(object):
	def __init__(self):
		self.agent_list =  [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]


	def process_request(self, request, spider):
		#print "**************************" + random.choice(self.agents)
		request.headers['User-Agent'] = random.choice(self.agent_list)

    
  

       