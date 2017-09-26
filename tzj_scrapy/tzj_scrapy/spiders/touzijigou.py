# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tzj_scrapy.items import TzjgItem
# from tzj_scrapy.utils.get1 import get_key
from urllib.parse import urljoin
# import io
# import sys

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TouzishijianSpider(scrapy.Spider):
	name = 'touzijigou'
	burl = "http://zdb.pedaily.cn"

	def start_requests(self):
		start_url = "http://zdb.pedaily.cn/company/all/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		sel = Selector(text=response.text)
		# sel.xpath('//dt[@class="industry"]/a')
		urls = sel.xpath('//a[@class="f16"]/@href').extract()
		url_list = [urljoin(self.burl, x) for x in urls if urls]
		for detail_url in url_list:
			yield scrapy.Request(detail_url, callback=self.get_detail)

		next_url = sel.xpath('//a[@class="next"][last()]/@href').extract_first()
		if next_url:
			nurl = urljoin(self.burl, next_url)
			yield scrapy.Request(nurl, callback=self.parse)

	def get_detail(self, response):
		item = TzjgItem()
		item['tz_jg_detail'] = response.url
		sel = Selector(text=response.text)
		# 投资机构logo
		tz_jg_logo = sel.xpath('//div[@class="img"]/img/@src').extract_first()

		# 投资机构基本信息
		info_tag = sel.xpath('//div[@class="info"]')
		tz_jg_name = info_tag.xpath('./h1/text()').extract_first()
		tz_jg_short = info_tag.xpath('./h1/em/text()').extract_first()
		tz_jg_en = info_tag.xpath('./h2/text()').extract_first()
		li_tags = info_tag.xpath('./ul/li')

		capital_type = li_tags[0].xpath('./text()').extract_first()
		tz_jg_property = li_tags[1].xpath('./text()').extract_first()
		tz_jg_regist_addr = li_tags[2].xpath('./text()').extract_first()
		tz_jg_create_time = li_tags[3].xpath('./text()').extract_first()
		tz_jg_headquarter = li_tags[4].xpath('./text()').extract_first()
		tz_jg_site = li_tags[5].xpath('./a/@href').extract_first()
		tz_jg_invest_stage = li_tags[6].xpath('./text()').extract_first()

		# 投资机构简介和联系方式
		tz_jg_intro_list = sel.xpath('//*[@id="desc"]/p//text()').extract()
		tz_jg_intro = ''.join(tz_jg_intro_list)
		p_tags = sel.xpath('//*[@id="contact"]/p')
		tz_jg_tel = ''
		tz_jg_fax = ''
		tz_jg_addr = ''
		tz_jg_postcode = ''
		for p_tag in p_tags:
			text = p_tag.xpath('./span/text()').extract_first()
			someone = p_tag.xpath('./text()').extract_first()
			if '联系电话' in text:
				tz_jg_tel = someone
			elif '传 真' in text:
				tz_jg_fax = someone
			elif '地 址' in text:
				tz_jg_addr = someone
			elif '邮 编' in text:
				tz_jg_postcode = someone

		# 团队信息
		t_li_tags = sel.xpath('//*[@id="team"]/ul/li')
		team_per_list = []
		for t_li_tag in t_li_tags:
			p_a_tag = t_li_tag.xpath('./div/a')
			team_per_url_half = p_a_tag.xpath('./@href').extract_first()
			team_per_url = urljoin(self.burl, team_per_url_half)
			team_per_face_half = p_a_tag.xpath('./div[@class="face"]/img/@src').extract_first()
			team_per_face = urljoin(self.burl, team_per_face_half)
			team_per_name = p_a_tag.xpath('./div[@class="mark-topic"]/text()').extract_first()
			team_per_duty = p_a_tag.xpath('./div[@class="mark-duty"]/text()').extract_first()
			team_per_dict = {'team_per_url': team_per_url, 'team_per_face': team_per_face, 'team_per_name': team_per_name, 'team_per_duty': team_per_duty}
			team_per_list.append(team_per_dict)

		# 投资事件
		tz_sj_tag = sel.xpath('//div[@id="inv-box"]')
		tz_sj_url_half = tz_sj_tag.xpath('./h3/a/@href').extract_first()
		tz_sj_url = urljoin(self.burl, tz_sj_url_half)
		tz_sj_li_tags = tz_sj_tag.xpath('./div/ul/li[position()>1]')
		tz_sj_list = []
		for tz_sj_li_tag in tz_sj_li_tags:
			# invest_time = tz_sj_li_tag.xpath('./div/span/text()').extract_first()
			rz_comp_url_half = tz_sj_li_tag.xpath('./dl/dt[@class="company"]/a/@href').extract_first()
			rz_comp_url = urljoin(self.burl, rz_comp_url_half)
			rz_comp_short = tz_sj_li_tag.xpath('./dl/dt[@class="company"]/a/text()').extract_first()
			tz_sj_detail_half = tz_sj_li_tag.xpath('./dl/dt[@class="view"]/a/@href').extract_first()
			tz_sj_detail = urljoin(self.burl, tz_sj_detail_half)
			tz_sj_dict = {'rz_comp_url': rz_comp_url, 'rz_comp_short': rz_comp_short, 'tz_sj_detail': tz_sj_detail}
			tz_sj_list.append(tz_sj_dict)

		# 募资事件
		mz_sj_tag = sel.xpath('//div[@id="pe-box"]')
		mz_sj_url_half = mz_sj_tag.xpath('./h3/a/@href').extract_first()
		mz_sj_url = urljoin(self.burl, mz_sj_url_half)
		mz_sj_li_tags = mz_sj_tag.xpath('./div/ul/li[position()>1]')
		mz_sj_list = []
		for mz_sj_li_tag in mz_sj_li_tags:
			mz_fund_url_half = mz_sj_li_tag.xpath('./dl/dt[@class="fund"]/a/@href').extract_first()
			mz_fund_url = urljoin(self.burl, mz_fund_url_half)
			mz_fund_short = mz_sj_li_tag.xpath('./dl/dt[@class="fund"]/a/text()').extract_first()
			mz_sj_detail_half = mz_sj_li_tag.xpath('./dl/dt[@class="view"]/a/@href').extract_first()
			mz_sj_detail = urljoin(self.burl, mz_sj_detail_half)
			mz_sj_dict = {'mz_fund_url': mz_fund_url, 'mz_fund_short': mz_fund_short, 'mz_sj_detail': mz_sj_detail}
			mz_sj_list.append(mz_sj_dict)

		item['tz_jg_logo'] = tz_jg_logo
		item['tz_jg_name'] = tz_jg_name
		item['tz_jg_short'] = tz_jg_short
		item['tz_jg_en'] = tz_jg_en
		item['capital_type'] = capital_type
		item['tz_jg_property'] = tz_jg_property
		item['tz_jg_regist_addr'] = tz_jg_regist_addr
		item['tz_jg_create_time'] = tz_jg_create_time
		item['tz_jg_headquarter'] = tz_jg_headquarter
		item['tz_jg_site'] = tz_jg_site
		item['tz_jg_invest_stage'] = tz_jg_invest_stage
		item['tz_jg_intro'] = tz_jg_intro
		item['tz_jg_tel'] = tz_jg_tel
		item['tz_jg_fax'] = tz_jg_fax
		item['tz_jg_addr'] = tz_jg_addr
		item['tz_jg_postcode'] = tz_jg_postcode
		item['team_per_list'] = str(team_per_list)
		item['tz_sj_url'] = tz_sj_url
		item['tz_sj_list'] = str(tz_sj_list)
		item['mz_sj_url'] = mz_sj_url
		item['mz_sj_list'] = str(mz_sj_list)


		yield item
