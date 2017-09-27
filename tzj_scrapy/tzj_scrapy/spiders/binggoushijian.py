# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tzj_scrapy.items import BgsjItem
# from tzj_scrapy.utils.get1 import get_key
from urllib.parse import urljoin
import io
import sys

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TouzishijianSpider(scrapy.Spider):
	name = 'binggoushijian'
	burl = "http://zdb.pedaily.cn"

	def start_requests(self):
		start_url = "http://zdb.pedaily.cn/ma/"
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
		item = BgsjItem()
		item['bg_sj_detail'] = response.url
		sel = Selector(text=response.text)
		info_tag = sel.xpath('//div[@class="info"]')
		bg_sj_title = info_tag.xpath('./h1/text()').extract_first()
		li_tags = info_tag.xpath('./ul/li')
		bg_gs_detail_half = li_tags[0].xpath('./a/@href').extract_first()
		bg_gs_detail = urljoin(self.burl, bg_gs_detail_half) if bg_gs_detail_half else ''
		bg_gs_name = li_tags[0].xpath('./a/text()|./text()').extract_first()
		bei_bg_gs_detail_half = li_tags[1].xpath('./a/@href').extract_first()
		bei_bg_gs_detail = urljoin(self.burl, bei_bg_gs_detail_half) if bei_bg_gs_detail_half else ''
		bei_bg_gs_name = li_tags[1].xpath('./a/text()|./text()').extract_first()

		bg_state = li_tags[2].xpath('./text()').extract_first()
		industry_url_half = li_tags[3].xpath('./a/@href').extract_first()
		industry_url = urljoin(self.burl, industry_url_half) if industry_url_half else ''
		industry = li_tags[3].xpath('./a/text()|./text()').extract_first()
		# 涉及股权
		equity_concern = li_tags[4].xpath('./text()').extract_first()
		bg_start_time = li_tags[5].xpath('./text()').extract_first()
		bg_finish_time = li_tags[6].xpath('./text()').extract_first()
		is_support = li_tags[7].xpath('./text()').extract_first()

		bg_sj_intro_list = sel.xpath('//div[@id="desc"]/p/text()').extract()
		bg_sj_intro = ''.join(bg_sj_intro_list)
		item['bg_sj_title'] = bg_sj_title
		item['bg_gs_detail'] = bg_gs_detail
		item['bg_gs_name'] = bg_gs_name
		item['bei_bg_gs_detail'] = bei_bg_gs_detail
		item['bei_bg_gs_name'] = bei_bg_gs_name
		item['bg_state'] = bg_state
		item['industry_url'] = industry_url
		item['industry'] = industry
		item['equity_concern'] = equity_concern
		item['bg_start_time'] = bg_start_time
		item['bg_finish_time'] = bg_finish_time
		item['is_support'] = is_support
		item['bg_sj_intro'] = bg_sj_intro

		yield item
