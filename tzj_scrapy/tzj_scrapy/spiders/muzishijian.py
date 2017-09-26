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

		for li_tag in li_tags:
			if '管理机构' in li_tag.xpath('./span/text()').extract_first():
				tz_jg_detail = li_tag.xpath('./a/@href').extract_first()
				tz_jg_name = li_tag.xpath('./a/text()').extract_first()
			else:
				pass

		rz_comp_url_half = sel.xpath('//li[@class="full"][1]/a/@href').extract_first()
		rz_comp_url = urljoin(self.burl, rz_comp_url_half)
		rz_comp_name = sel.xpath('//li[@class="full"][1]/a/text()').extract_first()

		tz_jg_tags = sel.xpath('//li[@class="full"]/a[starts-with(@href, "/company")]')
		tz_jg_list = []
		for tz_jg_tag in tz_jg_tags:
			tz_jg_url = tz_jg_tag.xpath('./@href').extract_first()
			tz_jg_name = tz_jg_tag.xpath('./text()').extract_first()
			tz_jg_dict = {"tz_jg_url": urljoin(self.burl, tz_jg_url), "tz_jg_name": tz_jg_name}
			tz_jg_list.append(tz_jg_dict)
		currency = sel.xpath('//span[@class="d"]/text()').extract_first()
		money = sel.xpath('//span[@class="m"]/text()').extract_first()
		loop = sel.xpath('//span[@class="b round"]/text()').extract_first()
		invest_time = sel.xpath('//div[@class="info"]//li[5]/text()').extract_first()
		indus_tags = sel.xpath('//div[@class="info"]//li[6]/a')
		indus_list = []
		for indus_tag in indus_tags:
			indus_url = indus_tag.xpath('./@href').extract_first()
			indus_name = indus_tag.xpath('./text()').extract_first()
			indus_dict = {"indus_url": urljoin(self.burl, indus_url), "indus_name": indus_name}
			indus_list.append(indus_dict)
		invest_intro_list = sel.xpath('//div[@id="desc"]/p/text()').extract()
		invest_intro = ''.join(invest_intro_list)
		item['tz_sj_title'] = tz_sj_title
		item['rz_comp_url'] = rz_comp_url
		item['rz_comp_name'] = rz_comp_name
		item['tz_jg_list'] = str(tz_jg_list)
		item['currency'] = currency
		item['money'] = money
		item['loop'] = loop
		item['invest_time'] = invest_time
		item['indus_list'] = str(indus_list)
		item['invest_intro'] = invest_intro

		yield item
