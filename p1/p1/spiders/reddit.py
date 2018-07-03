from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
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
# user comments xpath '//form[contains(@class,"usertext warn-on-unload")]'
class RedditSpider(Spider):
    name = 'reddit'
    # allowed_domains = ['reddit.com']
    # start_urls = ['http://reddit.com/']
    # def __init__(self):
    #     scrapy.Spider.__init__(self)
    #     # using a firefox driver, for production use we can use a PhantomJS browser.
    #     self.driver = webdriver.Firefox()
    def start_requests(self):
        # self.driver = webdriver.Chrome('C:/Users/carbon/Desktop/scrapy-modules/scraping/driver/chromedriver')
        # options = Options()
        # options.set_headless(headless=True)

        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy_type', 1)
        # profile.set_preference('network.proxy.http', "49.248.89.114")
        # profile.set_preference('network.proxy.http_port', 8080)
        profile.set_preference('network.proxy.http', "127.0.0.1")
        profile.set_preference('network.proxy.http_port', 9150)
        profile.update_preferences()
        binary = FirefoxBinary('C:/Users/carbon/Desktop/torbrowser/Browser/firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary,firefox_profile = profile)
        # self.driver = webdriver.Firefox(firefox_binary=binary)
        self.driver.get('https://reddit.com/login')
        # getting the search field by id using selenium, putting text and hit enter or search button
        # inputElement = self.driver.find_element_by_xpath('//a[@data-test-id="login-button"]')

        # login_button = self.driver.find_element_by_xpath('//a[@data-test-id="login-button"]')
        # login_button.click()
        # sleep(5)

        # username = self.driver.find_element_by_xpath('//input[@id="loginUsername"]')
        # password = self.driver.find_element_by_xpath('//input[@id="loginPassword"]')
        username = self.driver.find_element_by_xpath('//input[@id="loginUsername"]')
        password = self.driver.find_element_by_xpath('//input[@id="loginPassword"]')
        # find_element_by_id('where')
        username.send_keys('venomsonly')
        password.send_keys('Poonam25')
        password.send_keys(Keys.ENTER)
        sleep(15)
        # self.driver.get('https://reddit.com')
        # subscriptions = self.driver.find_element_by_xpath('//div[text()="subscriptions"]')
        search = self.driver.find_element_by_xpath('//input[@type="search"]')
        search.send_keys('hello')
        # print(subscriptions)

    def parse(self, response):
        pass
