# -*- coding: utf-8 -*-
import requests
import scrapy
import re #正则表达
from bs4 import BeautifulSoup
from scrapy.http import Request #一个单独的request模块，需跟进url时使用
from spider_frame.items import SpiderFrameItem ##自己定义的需保存字段

import random
import time 
import numpy as np

class Myspider(scrapy.Spider):
    
    handle_httpstatus_list = [403]
    
    name = 'spider_frame'
    
    
    #把市值排名前50的股吧url放入字典
    #股吧url形式为：http://guba.eastmoney.com/list,股票代码.html
    def start_requests(self): #不用start_url的化就得定义个函数：start_requests(self)
        #star_url = 'http://vip.stock.finance.sina.com.cn/datacenter/hqstat.html#ltsz' #新浪财经股票按市值排名的页面
        #这是一动态网页，我找到其json元素中request_url为：
        #http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/IO.XSRV2.CallbackList['b4VIm$HArIJ1qfKO']/Market_Center.getHQNodeDataNew?page=1&num=50&sort=nmc&asc=0&node=hs_a
        #上面区别主要在"page"字段那
        #一页有50个
        
        #打补丁
        round1 = 0
        
        for i in range(3):
            if i == 0:
                star_url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHSZZS&sty=SHSZZS&st=0&sr=-1&p=4&ps=50&js=var%20hhFXKbQO={pages:(pc),data:[(x)]}&code=000300&rt=51667885"
            if i == 1:
                star_url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHSZZS&sty=SHSZZS&st=0&sr=-1&p=5&ps=50&js=var%20hhFXKbQO={pages:(pc),data:[(x)]}&code=000300&rt=51667885"
            if i == 2:
                star_url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHSZZS&sty=SHSZZS&st=0&sr=-1&p=6&ps=50&js=var%20hhFXKbQO={pages:(pc),data:[(x)]}&code=000300&rt=51667885"
                #round1 = 1  #补丁
            content = requests.get(star_url).content
            #content类型为bytes比特流，Python已经严格区分了bytes和str两种数据类型，得要转换下
            
            #前3个已近搞定了
            flag = 0
            #先弄前5个
            for item in re.findall(r'"(.*?),',str(content)):
                if len(item.split("'")[0]) == 0:
                    continue
                
                #if round1 == 0:
                flag = flag+1
                if flag <= 0:
                    continue
                if flag >50: #3内已完毕
                    break
                print("curr_gu is: %d" %flag)
                guba_url = "http://guba.eastmoney.com/list,replace_num.html"
                guba_url = guba_url.replace('replace_num',item.split('"')[0])
                print(guba_url)
                #yield scrapy.http.Request(guba_url, callback=self.parse, meta={'initial_url':guba_url, 'page':1, 'flag':2, 'flag_1':0})
                
                #打补丁
                replace_str = '_'+str(200)+'.html'
                start_url = guba_url.replace('.html',replace_str)
                step_flag = 0 #为1时表示不必再向后以100为区间爬取
                post_page = 300
                step = 100
                new_post_page = 0
                while(step>=1):
                    print(step)
                    status_code = 0
                    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    
                    while(status_code != 200):
                        time.sleep(np.random.randint(1,2))
                        test_req = requests.get(url = start_url,headers = headers)
                        status_code = test_req.status_code
                        
                    soup =  BeautifulSoup(test_req.content, 'lxml')
                    comment_num = []  
                    urls = []
                    table = soup.find_all(class_ = 'articleh')
                    
                    for element in table:
                        if element.find(class_ = 'l3') == None: #置顶帖太多会显示“点击展开”，而置顶帖为官方号消息与该股吧无关，直接跳过
                            continue
                        comment_num.append(int(element.find(class_ = 'l2').text))
                        urls.append(element.find(class_ = 'l3').a['href'])
            
                    for i in range(len(comment_num)):
                        if 'cjpl' in urls[i] or 'ask' in urls[i] or 'gssz' in urls[i] or 'licai' in urls[i] or 'list' in urls[i]: #不是回帖，是咨询或问答等与该股无关的贴
                            continue
                        if comment_num[i]==0: #回帖为0，看其回帖日期
                            status_code = 0
                            while(status_code != 200):
                                time.sleep(np.random.randint(1,2))
                                post_url = "http://guba.eastmoney.com"+urls[i]
                                print('test_1')
                                print(post_url)
                                post_req = requests.get(url = post_url, headers = headers)
                                status_code = post_req.status_code
                            soup =  BeautifulSoup(post_req.content, 'lxml')
                            post_date = soup.find(class_ = "zwfbtime").text.split(' ')[1] 
                            post_year = int(post_date.split('-')[0])
                            print(post_year)
                            if post_year < 2018: #这页之后都不用爬了
                                step_flag = 1
                                
                                new_post_page = post_page - int(step/2)
                                start_url = start_url.replace('_'+str(post_page), '_'+str(new_post_page))
                                post_page = new_post_page
                                step = int(step/2)
                                
                                print("curr_page is: %d" %post_page)
                                break
                            else: #>=还要向后查看
                                new_post_page = post_page + step
                                start_url = start_url.replace('_'+str(post_page), '_'+str(new_post_page))
                                post_page = new_post_page
                                if step_flag == 1:
                                    step = int(step/2)
                              
                                print("curr_page is: %d" %post_page)
                                break
                    #都没有，基本上就是没页数了
                    new_post_page = post_page - int(step/2)
                    start_url = start_url.replace('_'+str(post_page), '_'+str(new_post_page))
                    post_page = new_post_page
                    step_flag = 1
                    step = int(step/2)
                    
                print(guba_url)
                
                for i in range(post_page):
                    replace_str = '_'+str(i+1)+'.html'
                    tiezi_url = guba_url.replace('.html',replace_str)
                    page = i+1
                    print("crawl tiezi in page: %d" %page)
                    #判断年份得放这：默认是2018 如果100页前出现1月2月那就是2019年
                    
                    yield scrapy.http.Request(tiezi_url, callback=self.parse, meta={'initial_url':guba_url,'page':page})
                
                
                #打补丁
                #yield scrapy.http.Request(guba_url, callback=self.parse, meta={'initial_url':guba_url, 'page':1, 'flag':2, 'flag_1':0})
                #break
            
            
    def parse(self,response): #respond的是每个股的股吧首页
        #items = []
        #有了股吧url后，现在是想爬取2年内所有回帖
        #初始为flag = 2, flag_1 = 0
        page = response.meta['page']
        #flag = response.meta['flag'] #先抓一年的试试
        #flag_1 = response.meta['flag_1']
        
        soup =  BeautifulSoup(response.text, 'lxml')
        title = []
        urls = []
        date = []
        comment_num = []  

        table = soup.find_all(class_ = 'articleh')
        
        stock_name = soup.find(id ="stockname").text.split('吧')[0]
        #if int(table[0].find(class_ = 'l5').text.split('-')[0]) == 12:   #第一次遇到开头第一个帖子的最近回复日期为12，表示跨了一年了
        #    if flag_1 == 0: #第一次碰到
        #        flag = flag-1
        #        flag_1 = 1
        #if int(table[0].find(class_ = 'l5').text.split('-')[0]) < 12:  #
        #    flag_1 = 0
            
        for element in table:
            if element.find(class_ = 'l3') == None: #置顶帖太多会显示“点击展开”，而置顶帖为官方号消息与该股吧无关，直接跳过
                continue
            title.append(element.find(class_ = 'l3').a['title'])
            urls.append(element.find(class_ = 'l3').a['href'])
            date.append(element.find(class_ = 'l6').text)
            comment_num.append(int(element.find(class_ = 'l2').text))
        #爬取每个帖子的文本
        for i in range(len(urls)):
            if 'cjpl' in urls[i] or 'ask' in urls[i] or 'gssz' in urls[i] or 'licai' in urls[i]: #不是回帖，是咨询或问答等与该股无关的贴
                continue
            
            if comment_num[i]==0: #回帖为0，没必要爬帖子内容了，直接把标题与日期送入对象
                print("tring to insert pipline")
                item = SpiderFrameItem()
                item['stock_name'] = stock_name
                if int(date[i].split('-')[0]) <= 2:
                    if page < 100:
                        item['stock_date'] = str(2019)+'-'+date[i]
                    item['stock_date'] = str(2018)+'-'+date[i]
                item['stock_date'] = str(2018)+'-'+date[i]
                #item['stock_date'] = str(2019-2+flag)+'-'+date[i] #年份是str(2019-所爬年份数+flag)
                item['stock_date_text'] = title[i]
                yield item #用迭代器将item内容送入管道（pipline）中
                continue
                    
            #开始爬取回帖
            #post_page_num = 1 #回帖页数，初始为1
            for k in range(int(np.ceil(comment_num[i]/30))): #一页最多有30个回帖
                replace_k = '_'+str(k+1)+'.'
                tem_url = urls[i]
                tem_url = tem_url.replace('.',replace_k)
                post_url = "http://guba.eastmoney.com"+tem_url
                yield scrapy.http.Request(post_url, callback=self.post_parse, meta={'page':k+1, 'stock_name':stock_name})
                #time.sleep(np.random.random())
                #post_req = requests.get(post_url)
                    
                
      
       
            
            
        #return items
            
    def post_parse(self,response): #respond的是每个股的股吧首页
        soup = BeautifulSoup(response.text, 'lxml')
        page = response.meta['page']
        stock_name = response.meta['stock_name']
        #把发帖人内容也放入文本
        if page == 1:
            post_text = soup.find(class_ = "stockcodec .xeditor").text.strip() #发帖人文本
            post_date = soup.find(class_ = "zwfbtime").text.split(' ')[1] 
            item = SpiderFrameItem()
            item['stock_name'] = stock_name
            item['stock_date'] = post_date #年份是str(2019-所爬年份数+flag)
            item['stock_date_text'] = post_text
            
            #yield item #用迭代器将item内容送入管道（pipline）中
                
            if int(post_date.split('-')[0])>=2018:
                yield item
            
        post_table = soup.find_all(class_ = 'zwlitx')
        for post_ele in post_table:
                
            #回帖内容
            post_text = post_ele.find_all(class_ = "short_text")[-1].text.strip() #回帖文本 有些回帖会引用其他人的回帖，因此find_all结果的最后一个元素才是所需文本
            post_date = post_ele.find(class_ = "zwlitime").text.split(' ')[1]  #发帖日期,为string
            if len(post_text)<2 : #无效文本
                continue   
            item = SpiderFrameItem()
            item['stock_name'] = stock_name
            item['stock_date'] = post_date #年份是str(2019-所爬年份数+flag)
            item['stock_date_text'] = post_text
            
            #yield item #用迭代器将item内容送入管道（pipline）中
            if int(post_date.split('-')[0])>=2018:
                yield item            
                    
            #回帖爬取完毕
            
                
            