## Web Crawler
This repo records some basic web crawlers demo when I was learning the technique

### File Catalog: 

- mzitu_crawler.py 
    - It's the **crawler** used to scrape the images from mzitu.com
    - After adding the proxies, the program can change IP when this IP doesn't work. The proxies makes the program more robust and scrape more images.
- get_proxies.py 
    - Scrape the proxies from Internet, and check whether they are useful for our work.
    - Proxies is extracted from http://www.xicidaili.com

### How to run

1. activate `python3` environment
2. build `images` dir in the current path
3. get proxies by executing the `get_proxies.py` file
4. run the crawler
5. waiting for the completion

### Reference:

1. github: [vimerzhao](https://gist.github.com/vimerzhao) / [**mzitu_spider.py**](https://gist.github.com/vimerzhao/8485f89978aba2e7d9a0f8d82c371643)
2. zhihu: [mzitu网站的反爬虫机制](https://zhuanlan.zhihu.com/p/35562945)
3. 

---

Notes are recorded in my github [pages](https://shuogh.github.io):

- [Error met in the programming](https://shuogh.github.io/2019/06/13/Error-Met-in-First-Crawler-Demo/) 

