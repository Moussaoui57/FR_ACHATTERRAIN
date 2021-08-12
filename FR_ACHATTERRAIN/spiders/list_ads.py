
# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
import urlparse
import scrapy
#from dict_data import *
#from Myutils import *
import requests
import re
from scrapy.linkextractors import LinkExtractor
import datetime

class CSMspider(CrawlSpider, scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': '2',
        'LOG_ENABLED': 'True',
        'HTTPCACHE_GZIP' : 'True',
        'COMPRESSION_ENABLED' : 'True',
    }

    today = datetime.date.today()
    name_variable = 'ADS_'+ (today.strftime("%Y_%m_%d")) 
    name = name_variable
    
    rotate_user_agent = True  
    allowed_domains = ["www.achat-terrain.com", "achat-terrain.com"]
 

    def start_requests(self):
        response1 = requests.get('https://www.achat-terrain.com/exports/all_sitemap.xml').text
        selector = scrapy.Selector(text=response1)
        urls_list = re.findall("(https[^<>\"]+)", response1)
        for link in urls_list:
            yield Request(link, self.parse)

    def parse(self, response):
        links = []
        try:
            ads_list = re.findall("(https[^<>\"]+)", response.body)
            for link in ads_list:
                if ("www.achat-terrain.com" in link):
                    if "/vente" in link: 
                        links.append(link)

                       #yield Request(link, self.parse)
                       #yield{"ANNONCE_LINK":link}
            
            with open("ads_v1.txt","a") as f:
                for l in links:
                    data = f.write(l+"\n")

        except:
            pass
