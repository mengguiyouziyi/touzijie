# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tzj_scrapy.items import SssjItem
# from tzj_scrapy.utils.get1 import get_key
from urllib.parse import urljoin
import io
import sys

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TouzishijianSpider(scrapy.Spider):
	name = 'shangshishijian'
	burl = "http://zdb.pedaily.cn"

	def start_requests(self):
		start_url = "http://zdb.pedaily.cn/ipo/p2"
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
		item = SssjItem()
		item['ss_sj_detail'] = response.url
		sel = Selector(text=response.text)
		info_tag = sel.xpath('//div[@class="info"]')
		ss_sj_title = info_tag.xpath('./h1/text()').extract_first()
		li_tags = info_tag.xpath('./ul/li')
		rz_gs_detail_half = li_tags[0].xpath('./a/@href').extract_first()
		rz_gs_detail = urljoin(self.burl, rz_gs_detail_half)
		rz_gs_name = li_tags[0].xpath('./a/text()').extract_first()
		rz_gs_industry_url_half = li_tags[1].xpath('./a/@href').extract_first()
		rz_gs_industry_url = urljoin(self.burl, rz_gs_industry_url_half)
		rz_gs_industry = li_tags[1].xpath('./a/text()').extract_first()
		tz_jg_name = li_tags[2].xpath('./text()').extract_first()
		rz_gs_ipo_time = li_tags[3].xpath('./text()').extract_first()
		rz_gs_issue_price = li_tags[4].xpath('./text()').extract_first()
		rz_gs_ipo_addr_url_half = li_tags[5].xpath('./a/@href').extract_first()
		rz_gs_ipo_addr_url = urljoin(self.burl, rz_gs_ipo_addr_url_half)
		rz_gs_ipo_addr = li_tags[5].xpath('./a/text()').extract_first()
		rz_gs_sirculation = li_tags[6].xpath('./text()').extract_first()
		rz_gs_stock_code = li_tags[7].xpath('./text()').extract_first()
		is_support = li_tags[8].xpath('./text()').extract_first()

		item['ss_sj_title'] = ss_sj_title
		item['rz_gs_detail'] = rz_gs_detail
		item['rz_gs_name'] = rz_gs_name
		item['rz_gs_industry_url'] = rz_gs_industry_url
		item['rz_gs_industry'] = rz_gs_industry
		item['rz_gs_ipo_time'] = rz_gs_ipo_time
		item['tz_jg_name'] = tz_jg_name
		item['rz_gs_issue_price'] = rz_gs_issue_price
		item['rz_gs_ipo_addr_url'] = rz_gs_ipo_addr_url
		item['rz_gs_ipo_addr'] = rz_gs_ipo_addr
		item['rz_gs_sirculation'] = rz_gs_sirculation
		item['rz_gs_stock_code'] = rz_gs_stock_code
		item['is_support'] = is_support

		yield item
