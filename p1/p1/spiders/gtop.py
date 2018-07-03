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
class GtopSpider(Spider):
    name = 'gtop'
    allowed_domains = ('google.com', )
    # start_urls = ['http://google.com/']
    def start_requests(self):
        self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
        self.driver.get('http://google.com')
        # getting the search field by id using selenium, putting text and hit enter or search button
        inputElement = self.driver.find_element_by_xpath('//input[@name="q"]')
        # find_element_by_id('where')
        inputElement.send_keys('crypto hacks')
        inputElement.send_keys(Keys.ENTER)

        list_1 = []
        ctr = 0

        while True:
            if len(list_1) < 3:
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

        for i in list_1_trim:
            print('Taking screenshottttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
            save_fullpage_screenshot(self.driver, i, 'C:/Users/carbon/Desktop/scrapy-modules/screenshot')

        self.driver.quit()
        page_titles = []
        for address in list_1_trim:
            self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
            self.driver.get(address)
            ctr += 1
            # self.driver.save_screenshot("screenshot"+ str(ctr) + ".png")


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

    def save_fullpage_screenshot(driver, url, output_path, tmp_prefix='selenium_screenshot', tmp_suffix='.png'):
        # """
        # Creates a full page screenshot using a selenium driver by scrolling and taking multiple screenshots,
        # and stitching them into a single image.
        # """

        # get the page
        driver.get(url)

        # get dimensions
        window_height = driver.execute_script('return window.innerHeight')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        num = int( math.ceil( float(scroll_height) / float(window_height) ) )

        # get temp files
        tempfiles = []
        for i in xrange( num ):
            fd,path = tempfile.mkstemp(prefix='{0}-{1:02}-'.format(tmp_prefix, i+1), suffix=tmp_suffix)
            os.close(fd)
            tempfiles.append(path)
            pass

        try:
            # take screenshots
            for i,path in enumerate(tempfiles):
                if i > 0:
                    driver.execute_script( 'window.scrollBy(%d,%d)' % (0, window_height) )

                driver.save_screenshot(path)
                pass

            # stitch images together
            stiched = None
            for i,path in enumerate(tempfiles):
                img = Image.open(path)

                w, h = img.size
                y = i * window_height

                if i == ( len(tempfiles) - 1 ):
                    img = img.crop((0, h-(scroll_height % h), w, h))
                    w, h = img.size
                    pass

                if stiched is None:
                    stiched = Image.new('RGB', (w, scroll_height))

                stiched.paste(img, (
                    0, # x0
                    y, # y0
                    w, # x1
                    y + h # y1
                ))
                pass
            stiched.save(output_path)
        finally:
            # cleanup
            for path in tempfiles:
                if os.path.isfile(path):
                    os.remove(path)
            pass

        return output_path
