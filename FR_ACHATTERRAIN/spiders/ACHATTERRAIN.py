# -*- coding: utf-8 -*-
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
import urlparse
import scrapy
#from dict_data import *
#from Myutils import *
import requests
import re
from FR_ACHATTERRAIN.items import FrAchatterrainItem
from scrapy.linkextractors import LinkExtractor
import datetime

class ACHATTERRAINspider(CrawlSpider, scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': '1',
        'LOG_ENABLED': 'True',
        'HTTPCACHE_GZIP' : 'True',
        'COMPRESSION_ENABLED' : 'True',
    }
    today = datetime.date.today()
    name_variable = 'ACHATTERRAIN_'+ (today.strftime("%Y_%m_%d")) 
    name = name_variable
    name= "ACHATTERRAIN_2021_02"
      
    rotate_user_agent = True  
    allowed_domains = ["www.achat-terrain.com", "achat-terrain.com"]
   
    def start_requests(self):
        f = open('ads.txt', 'r')
        lignes = f.readlines()
        f.close()
        for url in lignes:
            url = url.strip("%0A")
            yield Request(url.rstrip('\n\r'), self.parse)


    def parse(self, response):
        item = FrAchatterrainItem()
        
        item["ANNONCE_LINK"] = response.url
        item["FROM_SITE"] = "https://www.achat-terrain.com"
        item["ID_CLIENT"] = re.findall("([0-9]+)_fr.htm", response.url)
        try:
           item["ANNONCE_DATE"] = re.findall("Mise à jour le ([0-9]+/[0-9]+/[0-9]+)", response.body)[0].replace("/","-")
        except:
            item["ANNONCE_DATE"] = ""
        item["ACHAT_LOC"] = "1"
        try:
           item["CATEGORIE"] = response.xpath("//li[contains(@class , 'breadcrumb-item')]/a/span//text()").extract()[1]
           #item["MAISON_APT"] = "6" # Terrain by default (website is ACHATTERRAIN)
           if "bâtir" in item["CATEGORIE"]:
              item["MAISON_APT"] = "6"
           else:
              item["MAISON_APT"] = "12"
        except:
            item["CATEGORIE"] = ""
        item["NEUF_IND"] = "N"
        try:
           #item["NOM"] = response.xpath("//div[contains(@id, 'swiperAnnonceDetail')]/div[contains(@class, 'swiper-wrapper')]//@title").extract_first()
           item["NOM"] = ''.join(response.xpath("//h1[contains(@class, 'detailDescription_title')]/span//text()").extract()).replace("\n","").replace("  ","").replace('"','').replace(";","")
        except:
            item["NOM"] = ""
        try:
            item["CP"] = response.xpath("//meta[@itemprop='postalCode']/@content").extract_first().strip()
            item["CP"] = re.sub('\D','',item["CP"])
            item["CP"] = item["CP"].zfill(5)[0:5]
            item['DEPARTEMENT'] = item["CP"][0:2]
        except Exception as e:
            print(str(e))
            item["CP"] = None
            item['DEPARTEMENT'] = None
        try:
           item["VILLE"] = response.xpath("//meta[@itemprop='addressLocality']/@content").extract_first()
        except:
            item["VILLE"] = ""
        try:
           item["ANNONCE_TEXT"] = response.xpath("//meta[@itemprop='description']/@content").extract_first().replace("\n","").replace("\r","").replace('"','').replace(";","")
        except:
            item["ANNONCE_TEXT"] = ""
        try: 
            #surface = ''.join(response.xpath("//div[@class='detailDescription_specifications-item']/span//text()").extract()).replace("\xa0","")
            surface = response.xpath("//span[@class='detailDescription_title-land']//text()").extract_first()
            item["SURFACE_TERRAIN"] = ''.join(re.findall("Terrain ([0-9]+)",surface))
            item["M2_TOTALE"] = ''.join(re.findall("Maison ([0-9]+)",surface))
            if item["M2_TOTALE"] == "":
               terrain = re.sub('Terrain \D','',surface)
               item["SURFACE_TERRAIN"] = re.sub('\D','',terrain)                      
        except:
            #surface = response.xpath("//span[@class='detailDescription_title-land']//text()").extract_first().replace("\xa0","")
            #item["SURFACE_TERRAIN"] = ''.join(re.findall("Terrain ([0-9]+)",surface))
            item["M2_TOTALE"] = None
            item["SURFACE_TERRAIN"] = None
        item["PHOTO"] =len(response.css(".swiper img"))
        try: 
            piece = ''.join(response.xpath("//div[@class='detailDescription_specifications-item']//text()").extract())
            item["PIECE"] = ''.join(re.findall("Pi.* : ([0-9]+)",piece))
        except:
            item["PIECE"] = None        
        try:
           prix= response.xpath("//div[@class='detailDescription_specifications-item']/span[@itemprop='price']//text()").extract_first()
           item["PRIX"] = re.sub('\D','',prix).strip()
        except:
            item["PRIX"] = None
        item["PAYS_AD"] = "FR"
        item["PRO_IND"] = "Y"
        item["SELLER_TYPE"] = "Pro"
        try:
           item['MINI_SITE_URL'] = "https://www.achat-terrain.com" + response.xpath("//div[contains(@class, 'detailContactStatic_more')]/a//@href").extract_first()
           item['MINI_SITE_ID'] = ''.join(re.findall("-*([0-9]+)-", item['MINI_SITE_URL']))
        except:
            item['MINI_SITE_URL'] = None
            item['MINI_SITE_ID'] = None
        try:
            item['AGENCE_NOM'] = response.xpath("//div[contains(@class, 'detailContactStatic_name')]//text()").extract_first().strip()
        except:
            item['AGENCE_NOM'] = None
        try:
            item['AGENCE_ADRESSE'] = response.xpath("//div[contains(@class, 'detailContactStatic_address')]/text()").extract_first().strip().replace('"','').replace(";","").replace("\n"," ").replace("\r"," ")
        except:
            item['AGENCE_ADRESSE'] = None
        try:
            cp_vi = response.xpath("//div[contains(@class, 'detailContactStatic_address')]/text()").extract()[1]
            cp = re.sub('\D','',cp_vi)
            if len(cp) > 4:
               cp_ville = response.xpath("//div[contains(@class, 'detailContactStatic_address')]/text()").extract()[1]
               item['AGENCE_VILLE'] = re.sub('\d+','',cp_ville).strip() # keeps not digit
               item['AGENCE_CP'] = re.sub('\D','',cp_ville).strip().zfill(5)[0:5]  # keeps digits
            else:
               cp_ville = response.xpath("//div[contains(@class, 'detailContactStatic_address')]/text()").extract()[2]
               item['AGENCE_VILLE'] = re.sub('\d+','',cp_ville).strip() # keeps not digit
               item['AGENCE_CP'] = re.sub('\D','',cp_ville).strip().zfill(5)[0:5]  # keeps digits
        except:
            item['AGENCE_VILLE'] = None
            item['AGENCE_CP'] = None
        try:
            item['AGENCE_DEPARTEMENT'] = item["AGENCE_CP"][0:2]
        except:
            item['AGENCE_DEPARTEMENT'] = None
        try:
            item["AGENCE_TEL"] = response.xpath("//div[contains(@class, 'detailContactStatic_phone')]/a//@phone").extract_first().replace(" ","").replace(".","")
        except:
            item["AGENCE_TEL"] = None
 
        yield item

