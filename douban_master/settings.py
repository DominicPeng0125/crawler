# -*- coding: utf-8 -*-

"""
Scrapy settings for the douban_master project.

This configuration is designed for polite, distributed crawling using
Scrapy + scrapy-redis. It supports pause/resume, optional proxy rotation,
and adaptive throttling.
"""

import random

BOT_NAME = 'douban_master'

SPIDER_MODULES = ['douban_master.spiders']
NEWSPIDER_MODULE = 'douban_master.spiders'


# =========================
# Identity & Politeness
# =========================

# Identify the crawler clearly and responsibly
USER_AGENT = 'douban-master-crawler/1.0 (+https://github.com/yourusername/douban_master)'

# Always obey robots.txt in production
ROBOTSTXT_OBEY = True


# =========================
# Request Rate & Concurrency
# =========================

# Limit concurrency to reduce load on the target site
CONCURRENT_REQUESTS = 8

# Delay between requests to the same domain
DOWNLOAD_DELAY = 1.0

# Disable cookies unless explicitly needed
COOKIES_ENABLED = False


# =========================
# AutoThrottle (Adaptive Rate Control)
# =========================

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False


# =========================
# Default Headers
# =========================

ua_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
]

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': random.choice(ua_list),
}


# =========================
# Downloader Middlewares
# =========================

DOWNLOADER_MIDDLEWARES = {
    'douban_master.middlewares.RandomProxyMiddleware': 350,
}


# =========================
# Item Pipelines
# =========================

ITEM_PIPELINES = {
    'douban_master.pipelines.DoubanMasterPipeline': 300,
}


# =========================
# scrapy-redis (Distributed Crawling)
# =========================

# Use Redis-based duplicate filtering
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# Use Redis-based scheduler
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# Keep Redis queues to allow pause/resume
SCHEDULER_PERSIST = True

# Priority-based scheduling (default scrapy behavior)
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'


# =========================
# Redis Connection
# =========================

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# REDIS_URL = 'redis://:password@127.0.0.1:6379'


# =========================
# Proxy Configuration (Optional)
# =========================

# Define proxies directly (for local testing only — do NOT commit real proxies)
# PROXIES = [
#     'http://127.0.0.1:8080',
# ]

# Or specify a proxy file via environment variable or settings
# PROXIES_FILE = '/path/to/proxies.txt'
