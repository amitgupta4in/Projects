# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
import random
from time import sleep
class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    # allowed_domains = ['https://www.imdb.com/search/title']
    start_urls = ['https://www.imdb.com/search/title?adult=include&view=simple&count=250']
# 20443 loop
    urls = []
    item_count = 0
    def parse(self, response):
        x1=  response.xpath('//span[@class="lister-item-header"]/span/a[contains(@href,"title")]/@href').extract()
        next = response.xpath('//div[contains(@class,"lister list detail sub-list")]/div/div[@class="desc"]/a/@href').extract_first()
        next_url = 'https://imdb.com/search/title/'+next
        for i in x1:
            self.urls.insert(len(self.urls),('https://imdb.com' + i))
        for i in self.urls:
            print(i)
        self.item_count=len(self.urls)
        print(self.item_count)
        # print(next_url)
        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        # sleep(random.randint(5,11))
        while self.item_count > 1000:
            return 0
        yield Request(next_url)
