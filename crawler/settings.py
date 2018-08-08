""" costom config settings """
# 所有的配置都必须为大写


# RETRY_COUNT = 3

# RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

COOKIE_ENABLE = False

# TIMEOUT = 10

# DEFAULT_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;'
#               'q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
# }


MAX_REQUEST_SIZE = 10

# PROXY_INTERVAL = 5

# SCHEDULER_PATH = "mini_scrapy.core.scheduler.Scheduler"

# DOWNLOADER_PATH = "mini_scrapy.downloadmiddleware.downloader.Downloader"

# DUPEFILTER = "mini_scrapy.core.dupefilters.RFPDupeFilter"
#
BLOOMFILTER_SIZE = 10000000
#
BLOOMFILTER_HASH_COUNT = 10

MYSQL_HOST = '192.168.0.210'
MYSQL_DBNAME = 'db_nosebox'
MYSQL_USER = 'kettle'
MYSQL_PASSWORD = 'root'


DOWNLOAD_MIDDLEWARE = {
    "mini_scrapy.downloadmiddleware.downloadermiddleware.RetryMiddleware":1,
    "crawler.middleware.RandomHead":2

}

# LOCALIZTION = True
# LOCALIZTION_PAHT = 'request_seen.txt'