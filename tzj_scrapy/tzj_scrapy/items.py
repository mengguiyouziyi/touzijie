# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TzsjItem(scrapy.Item):
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


class RzgsItem(scrapy.Item):
	rz_gs_detail = scrapy.Field()
	rz_gs_logo = scrapy.Field()
	rz_gs_name = scrapy.Field()
	rz_gs_short = scrapy.Field()
	rz_gs_en = scrapy.Field()
	rz_gs_headquarter = scrapy.Field()
	rz_gs_regist_addr = scrapy.Field()
	rz_gs_create_time = scrapy.Field()
	rz_gs_industry = scrapy.Field()
	rz_gs_site = scrapy.Field()
	rz_gs_intro = scrapy.Field()
	rz_gs_fax = scrapy.Field()
	rz_gs_tel = scrapy.Field()
	rz_gs_postcode = scrapy.Field()
	rz_gs_addr = scrapy.Field()
	rz_sj_list = scrapy.Field()


class MzsjItem(scrapy.Item):
	"""
	item['mz_sj_detail'] = response.url
	item['mz_sj_title'] = mz_sj_title
	item['mz_fund_name'] = mz_fund_name
	item['currency'] = currency
	item['mz_sj_create_time'] = mz_sj_create_time
	item['mz_sj_state'] = mz_sj_state
	item['tz_jg_detail'] = tz_jg_detail
	item['tz_jg_name'] = tz_jg_name
	item['target_size'] = target_size
	item['capital_type'] = capital_type
	item['mz_sj_money'] = mz_sj_money
	item['prospectus_intro'] = invest_intro
	"""
	mz_sj_detail = scrapy.Field()
	mz_sj_title = scrapy.Field()
	mz_fund_name = scrapy.Field()
	currency = scrapy.Field()
	mz_sj_create_time = scrapy.Field()
	mz_sj_state = scrapy.Field()
	tz_jg_detail = scrapy.Field()
	tz_jg_name = scrapy.Field()
	target_size = scrapy.Field()
	capital_type = scrapy.Field()
	mz_sj_money = scrapy.Field()
	prospectus_intro = scrapy.Field()