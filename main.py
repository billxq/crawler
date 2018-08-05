#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @date: 2018/8/3 下午7:08
# @author: Bill
# @file: main.py
import csv
import os
import time
from urllib.parse import urlencode
from selenium import webdriver



class crawl(object):
    def __init__(self):
        self.boot()
        self.data = list()
        self.i = 1
        print("Crawling Page {}".format(self.i))


    def boot(self):
        self.driver = webdriver.Chrome()
        return self.driver

    def close(self):
        self.driver.quit()
        return

    def q(self,offset=35):
        part_url = 'https://music.163.com/discover/playlist/?'
        data = {
            "order": "hot",
            "cat": "全部",
            "limit": 35,
            "offset": offset
        }
        return part_url + urlencode(data)

    def getHtml(self,url):
        self.driver.get(url=url)
        self.driver.implicitly_wait(10)
        self.driver.switch_to_frame('contentFrame')
        pl = self.driver.find_elements_by_class_name('s-fc0')
        nb = self.driver.find_elements_by_class_name('nb')
        pl_url = self.driver.find_elements_by_class_name('s-fc0')
        for p,n,u in zip(pl,nb,pl_url):
            self.data.append({
                "playlist":p.text,
                "nb": n.text,
                "url": u.get_attribute('href')
            })
        time.sleep(2)
        while self.driver.find_element_by_class_name('znxt').get_attribute('href') != 'javascript:void(0)':
            self.i += 1
            print("Crawling Page {}".format(self.i))
            next_url = self.driver.find_element_by_class_name('znxt').get_attribute('href')
            return self.getHtml(next_url)

    def parse(self,data_list):
        for dic in data_list:
            if '万' in dic.get('nb'):
                if int(dic.get('nb').split('万')[0]) > 500:
                    self.writeToCsv(dic)

    def writeToCsv(self,dic):
        csv_header = ['playlist', 'nb', 'url']
        if not os.path.exists('163music.csv'):
            with open('163music.csv','w',encoding='utf-8') as f:
                dict_writer = csv.DictWriter(f,csv_header)
                dict_writer.writeheader()
                dict_writer.writerow(dic)
        with open('163music.csv', 'a', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, csv_header)
            dict_writer.writerow(dic)







s = crawl()
s.getHtml('http://music.163.com/discover/playlist')
data_list =s.data
s.parse(data_list)
s.close()



