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

class TorSpider(Spider):
    name = 'tor'
    allowed_domains = ('google.com', )
    # start_urls = ['http://google.com/']
    def start_requests(self):
        self.driver = webdriver.Firefox(':/Users/carbon/Desktop/scrapy-modules/geckodriver')
        self.driver.get('http://google.com')
        # getting the search field by id using selenium, putting text and hit enter or search button
        inputElement = self.driver.find_element_by_xpath('//input[@name="q"]')
        # find_element_by_id('where')
        inputElement.send_keys('crypto hacks')
        inputElement.send_keys(Keys.ENTER)

        list_1 = []

        while True:
            if len(list_1) < 30:
                sleep(3)
                sel = Selector(text=self.driver.page_source)
                items = sel.xpath('//div[contains(@class,"rc")]/h3[contains(@class,"r")]/a/@href').extract()
                for item in items:
                    list_1.insert(len(list_1),item)

                self.driver.find_element_by_xpath('//span[contains(text(),"Next")]').click()
            else:
                break

            # next_button = self.driver.find_element_by_xpath('//a[contains(@title,"View the next page of results")]')
            # next_button.click()
        list_1_trim = []
        for i in list_1:
            try:
                list_1_trim.insert(len(list_1_trim),i.replace('www.',''))
            except:
                pass

        self.driver.quit()
        page_titles = []
        for address in list_1_trim:
            self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
            self.driver.get(address)
            try:
                sleep(3)
                sel = Selector(text=self.driver.page_source)
                page_titles.insert(len(page_titles), sel.xpath('//head/title/text()').extract_first())

                self.driver.quit()
            except:
                page_titles.insert(len(page_titles),'')
                self.driver.quit()




        df = pd.DataFrame({'URLs':list_1_trim,'page_titles':page_titles})
        df.to_csv('gtop.csv')

    # def titles(address):
    #     self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
    #     self.driver.get('address')
    #     sel = Selector(text=self.driver.page_source)
    #     page_title = sel.xpath('//head/title/text()').extract_first()
    #
    #     self.driver.quit()




    def parse(self, response):
        pass
