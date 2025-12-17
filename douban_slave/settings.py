# -*- coding: utf-8 -*-

"""
Scrapy settings for the douban_slave project.

This configuration is designed for polite, distributed crawling using
Scrapy + scrapy-redis. It supports pause/resume, optional proxy rotation,
and adaptive throttling. It aligns with douban_master for consistent behavior.
"""

import random
import os

BOT_NAME = 'douban_slave'

SPIDER_MODULES = ['douban_slave.spiders']
NEWSPIDER_MODULE = 'douban_slave.spiders'


# =========================
# Identity & Politeness
# =========================

# Use a clear, responsible User-Agent that identifies this crawler
USER_AGENT = 'douban-slave-crawler/1.0 (+https://github.com/yourusername/douban_slave)'

# Always obey robots.txt in production
ROBOTSTXT_OBEY = True


# =========================
# Request Rate & Concurrency
# =========================

# Limit concurrency to reduce load on the target site
CONCURRENT_REQUESTS = 8

# Delay between requests to the same domain (seconds)
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

# Use a config-driven proxy middleware (optional)
DOWNLOADER_MIDDLEWARES = {
    'douban_slave.middlewares.RandomProxyMiddleware': 350,
}


# =========================
# Item Pipelines
# =========================

# For the slave we push scraped items into Redis for downstream processing
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300,
}


# =========================
# scrapy-redis (Distributed Crawling)
# =========================

# Use scrapy-redis duplicate filtering
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# Use scrapy-redis scheduler for distributed crawling
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# Keep Redis queues so crawls can be paused and resumed (do not clear queues)
SCHEDULER_PERSIST = True

# Priority-based scheduler (sorted set)
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'


# =========================
# Redis Connection
# =========================

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
# Use DB 1 for slave (change if you want to share DB)
REDIS_PARAMS = {'db': int(os.environ.get('REDIS_DB', 1))}
# Optional: REDIS_URL = 'redis://:password@127.0.0.1:6379'


# =========================
# Logging & Timeouts
# =========================

LOG_FILE = os.environ.get('SPIDER_LOG_FILE', "douban_slave.log")
LOG_LEVEL = os.environ.get('SPIDER_LOG_LEVEL', "INFO")

# Per-request download timeout (seconds)
DOWNLOAD_TIMEOUT = int(os.environ.get('DOWNLOAD_TIMEOUT', 30))


# =========================
# Proxy Configuration (Optional)
# =========================

# Define proxies directly (for local testing only — do NOT commit real proxies)
# PROXIES = [
#     'http://127.0.0.1:8080',
# ]

# Or specify a proxy file path via settings or environment variable (do not commit this file)
# PROXIES_FILE = '/path/to/proxies.txt'
# You can also set PROXIES_FILE using an env var:
# export PROXIES_FILE=/home/you/.config/douban/proxies.txt
