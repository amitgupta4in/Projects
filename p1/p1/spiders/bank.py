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
from xlsxwriter.workbook import Workbook
# Import the byte stream handler.
from io import BytesIO
from urllib.request import urlopen
class BankSpider(Spider):
    name = 'bank'
    def start_requests(self):
        link1='https://thebanks.eu/banks/16393'
        self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
        self.driver.get(link1)
        img = self.driver.find_element_by_xpath('//div[contains(@class,"row")]/div/div[contains(@class,"background-white")]/img')
        url = img.get_attribute('src')

        image_data = BytesIO(urlopen(url).read())
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('output/fancy.xlsx', engine='xlsxwriter')
        df = pd.DataFrame()
        df.to_excel(writer, index=False, sheet_name='report')

        # Get access to the workbook and sheet
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('B:B', 50)
        worksheet.set_row(1,50)
        worksheet.insert_image('B2', url, {'image_data': image_data,'x_scale': 0.5, 'y_scale': 0.5,'x_offset': 5, 'y_offset': 5})

        workbook.close()
        # df = pd.DataFrame({'one':image_data})
        # df.to_excel('output/img.xslx')
        # img_file = urllib.urlretrieve(src, "filename.png")
        print('ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
        # # sel = Selector(text=self.driver.page_source)
        # # //div[contains(@class,"row")]/div/div/img
        # # img = sel.xpath('//div[contains(@class,"row")]/div/div/img').extract_first()
        # from xlsxwriter.workbook import Workbook
        # # Create an new Excel file and add a worksheet.
        # workbook = Workbook('images.xlsx')
        # worksheet = workbook.add_worksheet()
        #
        # # Widen the first column to make the text clearer.
        # worksheet.set_column('A:A', 30)
        #
        # # Insert an image.
        # worksheet.write('A2', 'Insert an image in a cell:')
        # worksheet.insert_image('B2', src)
        #
        # workbook.close()
        # df = pd.DataFrame({'one':urllib.urlretrieve(src, "filename.png")})
        # df.to_excel('output/img.xslx')
    def parse(self, response):
        pass
