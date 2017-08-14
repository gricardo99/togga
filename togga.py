#!/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from random import randint
from regex import match
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

class ToggaSpider():

    def __init__(self):
        self.url_to_crawl = "https://www.playtogga.com/"
        self.all_items = []
        self.username = 'gabrielricardo'
        self.user_password = '4microe4'
        self.league = 'DD Hawks'

    # Open headless chromedriver
    def start_driver(self):
        print('starting driver...')
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.driver = webdriver.Chrome("/var/chromedriver/chromedriver")
        sleep(4)

    # Close chromedriver
    def close_driver(self):
        print('closing driver...')
        self.display.stop()
        self.driver.quit()
        print('closed!')

    # Tell the browser to get a page
    def get_home_page(self):
        print('getting page...')
        self.driver.get(self.url_to_crawl)
        sleep(randint(2,3))

    # Togga front gate page
    def login(self):
        print('getting login page...')
        try:
            self.driver.find_element_by_xpath('//*[@class="login"]').click()
            sleep(randint(2,3))
            form = self.driver.find_element_by_xpath('.//*[@class="email"]')
            form.find_element_by_xpath(".//input[@type='text']").send_keys(self.username)
            form.find_element_by_xpath(".//input[@type='password']").send_keys(self.user_password)
            form.find_element_by_xpath('.//button"]').click()
            sleep(randint(3,5))
        except Exception:
            pass

    def nav_to_league(self):
        self.driver.find_element_by_xpath('//*[@class="dropdown-component"]').click()
        league_match = '.*'+self.league+'.*'
        for league in self.driver.find_element_by_xpath('//*[@class="dropdown-item"]'):
            if match(league_match, league.text):
                league.click()
                print("click, going to league:"+self.league)
                sleep(randint(2,5))
                break

    def get_lineup(self):
        #lineup
        self.driver.find_element_by_xpath('//*[@routerlink="./lineup"]').click()
        print('grabbing current lineup...')
        #parse table
        trs = self.driver.find_elements(By.TAG_NAME, "tr") 
        for col in trs:
            tds = col.find_elements(By.TAG_NAME, "td")
            print('col name:'+col.text)
            for el in tds:
                print('ele:'+el.text)

    def process_elements(self, div):
        prd_image = ''
        prd_title = ''
        prd_price = ''

        try:
            prd_image = div.find_element_by_xpath('.//*[@class="photo item-photo"]').get_attribute("source")
            prd_title = div.find_element_by_xpath('.//*[@class="item-name ng-binding"]').text
            prd_price = div.find_element_by_xpath('.//*[@class="price ng-scope ng-binding"]').text
        except Exception:
            pass

        if prd_image and prd_title and prd_price:
            single_item_info = {
            'image': prd_image.encode('UTF-8'),
            'title': prd_title.encode('UTF-8'),
            'price': prd_price.encode('UTF-8')
            }
            return single_item_info
        else:
            return False

    def parse(self):
        self.start_driver()

        self.get_home_page()
        self.login()

        self.close_driver()

        if self.all_items:
            return self.all_items
        else:
            return False


# Run spider
Togga = ToggaSpider()
#items_list = Togga.parse()
Togga.start_driver()
Togga.get_home_page()
Togga.login()
Togga.nav_to_league()
Togga.get_lineup()


# Do something with the data touched
#for item in items_list:
#	print(item)
