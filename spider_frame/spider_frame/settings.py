# -*- coding: utf-8 -*-

# Scrapy settings for spider_frame project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

JOBDIR='pause'
 
#增加全局并发数
#CONCURRENT_REQUESTS = 100

DOWNLOAD_TIMEOUT = 8

BOT_NAME = 'spider_frame'

SPIDER_MODULES = ['spider_frame.spiders']
NEWSPIDER_MODULE = 'spider_frame.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider_frame (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 禁止cookies:
COOKIES_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}


# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
        #'spider_frame.middlewares.MyCustomDownloaderMiddleware': 543,
        'spider_frame.middlewares.ChangeProxy': 543,
        'spider_frame.middlewares.Random_Useragent': 542,
        #'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
        # Fix path to this module
        #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
}


#SPIDER_MIDDLEWARES = {
#    'myproject.middlewares.CustomSpiderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html

MONGO_HOST = "127.0.0.1"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "guba"  # 库名 
MONGO_COLL = "guba_text"  # collection名


ITEM_PIPELINES = {
    'spider_frame.pipelines.SpiderFramePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 301
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


RETRY_ENABLED = False
# Retry many times since proxies often fail
#RETRY_TIMES = 0
# Retry on most error codes since proxies fail for different reasons
#RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# Configure a delay for requests for the same website (default: 0)
#DOWNLOAD_DELAY=1
# Disable cookies (enabled by default)
#COOKIES_ENABLED=False
# Enable downloader middlewares

#关闭重定向:
REDIRECT_ENABLED = False


#启用Redis调度存储请求队列
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
 
#确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
 
#默认请求序列化使用的是pickle 但是我们可以更改为其他类似的。PS：这玩意儿2.X的可以用。3.X的不能用
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"
 
#不清除Redis队列、这样可以暂停/恢复 爬取
SCHEDULER_PERSIST = True #很重要，保存指纹队列在你下次爬取时可以去重
 
#使用优先级调度请求队列 （默认使用）
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
 
#最大空闲时间防止分布式爬虫因为等待而关闭
#这只有当上面设置的队列类是SpiderQueue或SpiderStack时才有效
#并且当您的蜘蛛首次启动时，也可能会阻止同一时间启动（由于队列为空）
#SCHEDULER_IDLE_BEFORE_CLOSE = 10
 
#将清除的项目在redis进行处理
#ITEM_PIPELINES = {
#    'scrapy_redis.pipelines.RedisPipeline': 300
#}
 
#序列化项目管道作为redis Key存储
#REDIS_ITEMS_KEY = '%(spider)s:items'
 
#默认使用ScrapyJSONEncoder进行项目序列化
#You can use any importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'
 
#指定连接到redis时使用的端口和地址（可选）
#REDIS_HOST = 'localhost'
#REDIS_PORT = 6379
 
#指定用于连接redis的URL（可选）
#如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
#REDIS_URL = 'redis://user:pass@hostname:9001'
 
#自定义的redis参数（连接超时之类的）
#REDIS_PARAMS  = {}
 
#自定义redis客户端类
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'
 
#如果为True，则使用redis的'spop'进行操作。
#如果需要避免起始网址列表出现重复，这个选项非常有用。开启此选项urls必须通过sadd添加，否则会出现类型错误。
#REDIS_START_URLS_AS_SET = False
 
#RedisSpider和RedisCrawlSpider默认 start_usls 键
#REDIS_START_URLS_KEY = '%(name)s:start_urls'
 
#设置redis使用utf-8之外的编码
#REDIS_ENCODING = 'latin1'



