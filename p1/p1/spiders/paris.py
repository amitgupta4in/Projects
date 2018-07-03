# -*- coding: utf-8 -*-
from time import sleep
import string
import re

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


class ParisSpider(Spider):
    name = 'paris'
    def start_requests(self):

        link1='https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-Paris_Ile_de_France.html'
        self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
        self.driver.get(link1)
        sel = Selector(text=self.driver.page_source)
        # self.driver.quit()
        # # getting the search field by id using selenium, putting text and hit enter or search button
        one = sel.xpath('//div[contains(@class,"listing_title")]/a/text()').extract()
        one_link = sel.xpath('//div[contains(@class,"listing_title ")]/a/@href').extract()
        two = sel.xpath('//div[contains(@class,"listing_rating")]/div/div/span/a/text()').extract()
        three  = sel.xpath('//div[contains(@class,"p13n_reasoning_v2")]/a/span/text()').extract()

        # four  = sel.xpath('//div[contains(@class,"p13n_reasoning_v2")]').extract()
        # for f in four:
        #     ss = Selector(text=f)
        #     text1=ss.xpath('//a/span/text()').extract()
        #     t = ''
        #     for i in text1:
        #         try:
        #             if len(i) <1:
        #                 t = t + '-'
        #             else:
        #                 t = t + i+'    '
        #         except:
        #             pass
        #     print(t)




        # for i in four:
        #     sel = Selector(text=four)
        #
        # print(len(one))
        # print('oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
        # for i in one_link:
        #     print('https://www.tripadvisor.fr'+i)
        # for i in three:
        #     print(i)


        list1=[]
        list2=[]
        list3=[]
        list4=[]
        ctr = 0
        # //div[contains(@class,"listing_info")]/div[contains(@class,"listing_title")]/a[contains(@href,"QQQ")]
        while True:
            if len(list1) < 10:
                sleep(3)
                sel = Selector(text=self.driver.page_source)
                one = sel.xpath('//div[contains(@class,"listing_title")]/a/text()').extract()
                one_link = sel.xpath('//div[contains(@class,"listing_title ")]/a/@href').extract()
                two = sel.xpath('//div[contains(@class,"listing_rating")]/div/div/span/a/text()').extract()

                for item in one:
                    list1.insert(len(list1),item)

                for item in two:
                    i = str(item.strip())
                    i = str(i.replace("avis", ""))
                    i = str(i.replace(" ", ""))
                    i = re.sub(r"\s+", "", i, flags=re.UNICODE)
                    # print(i)
                    list2.insert(len(list2),i)

                three  = sel.xpath('//div[contains(@class,"p13n_reasoning_v2")]').extract()
                for f in three:
                    ss = Selector(text=f)
                    text1=ss.xpath('//a/span/text()').extract()
                    t = ''
                    count_string = 0
                    for i in text1:
                        count_string +=1
                        print(count_string)
                        if count_string == 1:
                            print(text1[0])
                        if count_string == 2:
                            print(text1[0]+', '+text1[1])
                            # print(text1[1])
                    #     for j range(count_string):
                    #
                    #
                    # for i in text1:
                    #     print(len(i))
                        # try:
                        #     if len(i) <1:
                        #         t = t + '-'
                        #     else:
                        #         t = t + i+',,,'
                        # except:
                        #     pass
                    list3.insert(len(list3),t)

                # for item in one_link:
                #     list4.insert(len(list4),item)
                #
                #
                #
                # self.driver.find_element_by_xpath('//a[contains(@class,"nav next rndBtn ui_button primary taLnk")]').click()
            else:
                break
        # df = pd.DataFrame({'one':list1,'two':list2,'three':list3,'four':list4})
        # df.to_csv('output/paris.csv')

    def parse(self, response):
        pass
