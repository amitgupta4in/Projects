# -*- coding: utf-8 -*-
import scrapy


class ScreenshotSpider(scrapy.Spider):
    name = 'screenshot'
    def start_requests(self):
        self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
        self.driver.get('http://google.com')
        
        self.driver.get('http://google.com')

    def parse(self, response):
        pass
