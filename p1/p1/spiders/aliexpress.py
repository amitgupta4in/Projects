# -*- coding: utf-8 -*-
from time import sleep

import pandas as pd
from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
class AliexpressSpider(Spider):
    name = 'aliexpress'
    # allowed_domains = ['aliexpress.com']
    start_urls = ['https://aliexpress.com']
# //a[contains(@class,"history-item")]/@title
# //input[contains(@id,"search-key")]/@value
# //input[contains(@name,"SearchText")]/@value
    list_1 = []
    list_2 = []
    counter = 0
    pages = 2
    def parse(self, response):
        # search_box = response.xpath('//input[contains(@name,"SearchText")]/@value')
        return FormRequest.from_response(response,
                                         formdata={'SearchText': "jeans"
                                                   },
                                         callback=self.scrape_home_page)


    def scrape_home_page(self, response):
        # open_in_browser(response)
        # extract data from the first result page

        items = response.xpath('//h3/a[contains(@class,"history-item product")]/@title').extract()
        items_price = response.xpath('//span[contains(@itemprop,"price")]/text()').extract()
        for it in items:
            self.list_1.insert(len(self.list_1),it)
        for it in items_price:
            self.list_2.insert(len(self.list_2),it)

        self.counter += 1
        try:
            if self.counter == self.pages:
                df = pd.DataFrame({'items':self.list_1, 'price':self.list_2})
                df.to_csv('output/as.csv')
                return
            next_url ='https:'+ (response.xpath('//a[contains(@class,"page-next ui-pagination-next")]/@href').extract_first()).replace('www.','')
            print(next_url+"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            yield Request(next_url, callback=self.scrape_home_page)
        except:
            df = pd.DataFrame({'items':self.list_1,'price':self.list_2})
            df.to_csv('output/as.csv')



    def to_csv():
        df = pd.DataFrame({'items':self.list_1})
        df.to_csv('output/as.csv')
        pass
        # yield {'items': items,}
        # pass
        # l = ItemLoader(item=QuotesSpiderItem(), response=response)
        #
        # h1_tag = response.xpath('//h1/a/text()').extract_first()
        # tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        #
        # l.add_value('h1_tag', h1_tag)
        # l.add_value('tags', tags)
        #
        # return l.load_item()
