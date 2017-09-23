# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TzsjItem(scrapy.Item):
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


class TzjgItem(scrapy.Item):
	tz_jg_detail = scrapy.Field()
	tz_jg_logo = scrapy.Field()
	tz_jg_name = scrapy.Field()
	tz_jg_short = scrapy.Field()
	tz_jg_en = scrapy.Field()
	capital_type = scrapy.Field()
	tz_jg_property = scrapy.Field()
	tz_jg_regist_addr = scrapy.Field()
	tz_jg_create_time = scrapy.Field()
	tz_jg_headquarter = scrapy.Field()
	tz_jg_site = scrapy.Field()
	tz_jg_invest_stage = scrapy.Field()

	tz_jg_intro = scrapy.Field()
	tz_jg_tel = scrapy.Field()
	tz_jg_fax = scrapy.Field()
	tz_jg_addr = scrapy.Field()
	tz_jg_postcode = scrapy.Field()
	team_per_list = scrapy.Field()
	tz_sj_url = scrapy.Field()
	tz_sj_list = scrapy.Field()
	mz_sj_url = scrapy.Field()
	mz_sj_list = scrapy.Field()
