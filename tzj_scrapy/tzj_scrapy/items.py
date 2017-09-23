# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TzjScrapyItem(scrapy.Item):
    """
    item['detail_url'],item['tz_sj_title'],item['rz_comp_url'],item['rz_comp_name'],item['tz_jg_list'],item['currency'],item['money'],item['loop'],item['invest_time'],item['indus_list'],item['invest_intro']
    """
    detail_url = scrapy.Field()
    tz_sj_title = scrapy.Field()
    rz_comp_url = scrapy.Field()
    rz_comp_name = scrapy.Field()
    tz_jg_list = scrapy.Field()
    currency = scrapy.Field()
    money = scrapy.Field()
    loop = scrapy.Field()
    invest_time = scrapy.Field()
    indus_list = scrapy.Field()
    invest_intro = scrapy.Field()
