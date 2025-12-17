# Douban Distributed Web Crawler

A distributed web crawling system built with **Scrapy** and **scrapy-redis**, consisting of a **master** crawler that seeds URLs and one or more **slave** crawlers that consume and process those URLs in parallel.

This project was built for learning and demonstration purposes and focuses on distributed scheduling, fault tolerance, and production-safe crawling practices.

---

## Architecture Overview

The system is composed of two logical components:

### 1. douban_master
- Generates and seeds initial crawl URLs.
- Pushes URLs into Redis queues.
- Acts as the **controller / coordinator** of the crawl.
- Can be run independently or restarted without losing state.

### 2. douban_slave
- Consumes URLs from Redis.
- Fetches and parses pages in parallel.
- Pushes extracted items back into Redis for downstream processing.
- Multiple slave instances can run concurrently for horizontal scaling.

All coordination (queues, deduplication, scheduling) is handled by **Redis**, enabling:
- Distributed crawling
- Pause & resume
- Horizontal scaling across machines

---

## Technology Stack

- **Python 3.8+**
- **Scrapy** – high-level web crawling framework
- **scrapy-redis** – Redis-backed scheduler and duplicate filter
- **Redis** – distributed queue, scheduler, and state store

---

## Key Features

- Distributed crawling with Redis-backed scheduling
- Redis-based duplicate request filtering
- Pause and resume support (persistent queues)
- Optional proxy rotation (configuration-driven)
- Polite crawling practices:
  - robots.txt compliance
  - rate limiting
  - adaptive throttling (AutoThrottle)
- Clean separation between URL seeding (master) and data processing (slave)

---

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Redis server (local or remote)

### Install dependencies
```bash
pip install -r requirements.txt
