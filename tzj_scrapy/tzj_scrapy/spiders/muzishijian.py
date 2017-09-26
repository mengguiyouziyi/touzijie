# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tzj_scrapy.items import MzsjItem
# from tzj_scrapy.utils.get1 import get_key
from urllib.parse import urljoin
import io
import sys

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TouzishijianSpider(scrapy.Spider):
	name = 'muzishijian'
	burl = "http://zdb.pedaily.cn"

	def start_requests(self):
		start_url = "http://zdb.pedaily.cn/pe/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		sel = Selector(text=response.text)
		urls = sel.xpath('//dt[@class="view"]/a/@href').extract()
		url_list = [urljoin(self.burl, x) for x in urls if urls]
		for detail_url in url_list:
			yield scrapy.Request(detail_url, callback=self.get_detail)

		next_url = sel.xpath('//a[@class="next"][last()]/@href').extract_first()
		if next_url:
			nurl = urljoin(self.burl, next_url)
			yield scrapy.Request(nurl, callback=self.parse)

	def get_detail(self, response):
		item = MzsjItem()
		item['mz_sj_detail'] = response.url
		sel = Selector(text=response.text)
		info_tag = sel.xpath('//div[@class="info"]')
		mz_sj_title = info_tag.xpath('./h1/text()').extract_first()
		li_tags = info_tag.xpath('./ul/li')
		mz_fund_name = li_tags[0].xpath('./text()').extract_first()
		currency = li_tags[1].xpath('./text()').extract_first()
		mz_sj_create_time = li_tags[3].xpath('./text()').extract_first()
		mz_sj_state = li_tags[4].xpath('./text()').extract_first()
		tz_jg_detail_half = li_tags[5].xpath('./a/@href').extract_first()
		tz_jg_detail = urljoin(self.burl, tz_jg_detail_half)
		tz_jg_name = li_tags[5].xpath('./a/text()').extract_first()
		target_size = li_tags[6].xpath('./text()').extract_first()
		capital_type = li_tags[7].xpath('./text()').extract_first()
		mz_sj_money = li_tags[8].xpath('./text()').extract_first()

		invest_intro_list = sel.xpath('//div[@id="desc"]/p/text()').extract()
		invest_intro = ''.join(invest_intro_list)
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

		yield item
