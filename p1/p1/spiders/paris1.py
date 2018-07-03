# -*- coding: utf-8 -*-
from time import sleep
import string
import re
import random
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
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa30-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa60-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa90-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa120-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa150-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa180-Paris_Ile_de_France.html#FILTERED_LIST
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa210-Paris_Ile_de_France.html#FILTERED_LIST
# last page
## https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa570-Paris_Ile_de_France.html#FILTERED_LIST



class Paris1Spider(Spider):
    name = 'paris1'
    def start_requests(self):

        link1='https://www.tripadvisor.fr/Attractions-g187147-Activities-c41-Paris_Ile_de_France.html'
        # link1='https://www.tripadvisor.fr/Attractions-g187147-Activities-c42-oa570-Paris_Ile_de_France.html#FILTERED_LIST'
        self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
        self.driver.get(link1)
        sel = Selector(text=self.driver.page_source)
        # self.driver.quit()
        one = sel.xpath('//div[contains(@class,"listing_title")]/a/text()').extract()
        one_link = sel.xpath('//div[contains(@class,"listing_title ")]/a/@href').extract()
        two = sel.xpath('//div[contains(@class,"listing_rating")]/div/div/span/a/text()').extract()
        three  = sel.xpath('//div[contains(@class,"p13n_reasoning_v2")]/a/span/text()').extract()

        list1=[]
        list2=[]
        list3=[]
        list4=[]
        while True:
            if len(list1) < 600:
                sleep(random.randint(15,20))
                sel = Selector(text=self.driver.page_source)
                one = sel.xpath('//div[contains(@class,"listing_title")]/a/text()').extract()
                one_link = sel.xpath('//div[contains(@class,"listing_title ")]/a/@href').extract()
                two = sel.xpath('//div[contains(@class,"listing_info")]').extract()
                # print(two)
                # two = sel.xpath('//div[contains(@class,"listing_rating")]/div/div/span/a/text()').extract()

                for item in one:
                    list1.insert(len(list1),item)


                for item in two:
                    ss = Selector(text=item)
                    text1 = str(ss.xpath('//a[contains(text(), "avis")]/text()').extract_first())
                    # print(text1)
                    # if text1 == 'None':
                    #     list2.insert(len(list2),str('0'))
                    # else:
                    try:
                        if text1 != 'None':
                            i = str(text1.strip())
                            i = str(i.replace("avis", ""))
                            i = str(i.replace(" ", ""))
                            i = re.sub(r"\s+", "", i, flags=re.UNICODE)
                            # print(i)
                            list2.insert(len(list2),i)
                        else:
                            list2.insert(len(list2),str('0'))
                    except:
                        list2.insert(len(list2),str('0'))
                        pass



                three  = sel.xpath('//div[contains(@class,"p13n_reasoning_v2")]').extract()
                for f in three:
                    ss = Selector(text=f)
                    text1=ss.xpath('//a/span/text()').extract()
                    t = ' '
                    count_string = 0
                    for i in text1:
                        count_string +=1
                        # print(count_string)
                    if count_string == 2:
                        list3.insert(len(list3),str(text1[0]+', '+text1[1]))
                    elif count_string == 1:
                        list3.insert(len(list3),str(text1[0]))
                    else:
                        list3.insert(len(list3),'')


                for item in one_link:
                    list4.insert(len(list4),str('https://www.tripadvisor.fr')+item)
                try:
                    self.driver.find_element_by_xpath('//a[contains(@class,"nav next")]').click()
                except:
                    print(len(list1))
                    print(len(list2))
                    print(len(list3))
                    print(len(list4))
                    df = pd.DataFrame({'one':list1,'two':list2,'three':list3,'four':list4})
                    df.to_csv('output/Cours et ateliers à Paris.csv')
                    # self.driver.quit()
                    break

            else:
                break
        # print(len(list1))
        # print(len(list2))
        # print(len(list3))
        # print(len(list4))
        # df = pd.DataFrame({'one':list1,'two':list2,'three':list3,'four':list4})
        # df.to_csv('output/paris.csv')
        # self.driver.quit()

    def parse(self, response):
        pass
