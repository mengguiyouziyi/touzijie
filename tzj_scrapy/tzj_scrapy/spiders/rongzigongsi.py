# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tzj_scrapy.items import RzgsItem
# from tzj_scrapy.utils.get1 import get_key
from urllib.parse import urljoin
import io
import sys

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TouzishijianSpider(scrapy.Spider):
	name = 'rongzigongsi'
	burl = "http://zdb.pedaily.cn"

	def start_requests(self):
		start_url = "http://zdb.pedaily.cn/enterprise/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		sel = Selector(text=response.text)
		urls = sel.xpath('//a[@class="f16"]/@href').extract()
		url_list = [urljoin(self.burl, x) for x in urls if urls]
		for detail_url in url_list:
			yield scrapy.Request(detail_url, callback=self.get_detail)

		next_url = sel.xpath('//a[@class="next"][last()]/@href').extract_first()
		if next_url:
			nurl = urljoin(self.burl, next_url)
			yield scrapy.Request(nurl, callback=self.parse)

	def get_detail(self, response):
		item = RzgsItem()
		item['rz_gs_detail'] = response.url
		sel = Selector(text=response.text)
		# 融资公司logo
		rz_gs_logo = sel.xpath('//div[@class="img"]/img/@src').extract_first()

		# 融资公司基本信息
		info_tag = sel.xpath('//div[@class="info"]')
		rz_gs_name = info_tag.xpath('./h1/text()').extract_first()
		rz_gs_short = info_tag.xpath('./h1/em/text()').extract_first()
		rz_gs_en = info_tag.xpath('./h2/text()').extract_first()

		li_tags = info_tag.xpath('./ul/li')
		# 融资公司总部
		rz_gs_headquarter = li_tags[0].xpath('./text()').extract_first()
		rz_gs_regist_addr = li_tags[1].xpath('./text()').extract_first()
		rz_gs_create_time = li_tags[2].xpath('./text()').extract_first()
		rz_gs_industry = li_tags[3].xpath('./text()').extract_first()
		rz_gs_site = li_tags[4].xpath('./a/@href').extract_first() if len(li_tags) > 4 else ''

		# 融资公司简介和联系方式
		rz_gs_intro_list = sel.xpath('//*[@id="desc"]/p//text()').extract()
		rz_gs_intro = ''.join(rz_gs_intro_list)
		text_tags = sel.xpath('//*[@id="contact"]/p/text()').extract()
		span_tags = sel.xpath('//*[@id="contact"]/p/span/text()').extract()
		rz_gs_fax = ''
		rz_gs_tel = ''
		rz_gs_postcode = ''
		rz_gs_addr = ''
		for text, someone in zip(span_tags, text_tags):
			if '传 真' in text:
				rz_gs_fax = someone
			elif '联系电话' in text:
				rz_gs_tel = someone
			elif '邮政编码' in text:
				rz_gs_postcode = someone
			elif '详细地址' in text:
				rz_gs_addr = someone

		# 融资事件
		rz_sj_tag = sel.xpath('//div[@id="inv-box"]')
		rz_sj_li_tags = rz_sj_tag.xpath('./div/ul/li[position()>1]')
		rz_sj_list = []
		for rz_sj_li_tag in rz_sj_li_tags:
			# invest_time = tz_sj_li_tag.xpath('./div/span/text()').extract_first()
			rz_comp_url_half = rz_sj_li_tag.xpath('./dl/dt[@class="company"]/a/@href').extract_first()
			rz_comp_url = urljoin(self.burl, rz_comp_url_half)
			rz_comp_short = rz_sj_li_tag.xpath('./dl/dt[@class="company"]/a/text()').extract_first()
			rz_sj_detail_half = rz_sj_li_tag.xpath('./dl/dt[@class="view"]/a/@href').extract_first()
			rz_sj_detail = urljoin(self.burl, rz_sj_detail_half)
			rz_sj_dict = {'rz_comp_url': rz_comp_url, 'rz_comp_short': rz_comp_short, 'rz_sj_detail': rz_sj_detail}
			rz_sj_list.append(rz_sj_dict)

		item['rz_gs_logo'] = rz_gs_logo
		item['rz_gs_name'] = rz_gs_name
		item['rz_gs_short'] = rz_gs_short
		item['rz_gs_en'] = rz_gs_en
		item['rz_gs_headquarter'] = rz_gs_headquarter
		item['rz_gs_regist_addr'] = rz_gs_regist_addr
		item['rz_gs_create_time'] = rz_gs_create_time
		item['rz_gs_industry'] = rz_gs_industry
		item['rz_gs_site'] = rz_gs_site
		item['rz_gs_intro'] = rz_gs_intro
		item['rz_gs_fax'] = rz_gs_fax
		item['rz_gs_tel'] = rz_gs_tel
		item['rz_gs_postcode'] = rz_gs_postcode
		item['rz_gs_addr'] = rz_gs_addr
		item['rz_sj_list'] = str(rz_sj_list)


		yield item
