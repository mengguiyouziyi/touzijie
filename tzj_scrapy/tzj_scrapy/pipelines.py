# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from tzj_scrapy.items import TzsjItem, TzjgItem, RzgsItem


class MysqlPipeline(object):
	"""
	本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""

	def __init__(self):
		self.conn = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		# if spider.name == 'touzishijian':
		if isinstance(item, TzsjItem):
			# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """insert into touzijie_touzishijian (detail_url, tz_sj_title, rz_comp_url, rz_comp_name, tz_jg_list, currency, money, invest_loop, invest_time, indus_list, invest_intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [
				item['detail_url'], item['tz_sj_title'], item['rz_comp_url'], item['rz_comp_name'], item['tz_jg_list'],
				item['currency'], item['money'], item['loop'], item['invest_time'], item['indus_list'],
				item['invest_intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['detail_url'])
		elif isinstance(item, TzjgItem):
			sql = """insert into touzijie_touzijigou (tz_jg_detail,tz_jg_logo,tz_jg_name,tz_jg_short,tz_jg_en,capital_type,tz_jg_property,tz_jg_regist_addr,tz_jg_create_time,tz_jg_headquarter,tz_jg_site,tz_jg_invest_stage,tz_jg_intro,tz_jg_tel,tz_jg_fax,tz_jg_addr,tz_jg_postcode,team_per_list,tz_sj_url,tz_sj_list,mz_sj_url,mz_sj_list) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [item['tz_jg_detail'], item['tz_jg_logo'], item['tz_jg_name'], item['tz_jg_short'], item['tz_jg_en'],
			        item['capital_type'],
			        item['tz_jg_property'], item['tz_jg_regist_addr'], item['tz_jg_create_time'],
			        item['tz_jg_headquarter'], item['tz_jg_site'], item['tz_jg_invest_stage'], item['tz_jg_intro'],
			        item['tz_jg_tel'], item['tz_jg_fax'], item['tz_jg_addr'], item['tz_jg_postcode'],
			        item['team_per_list'], item['tz_sj_url'], item['tz_sj_list'], item['mz_sj_url'], item['mz_sj_list']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['tz_jg_detail'])
		elif isinstance(item, RzgsItem):
			sql = """insert into touzijie_rongzigongsi (rz_gs_detail,rz_gs_logo,rz_gs_name,rz_gs_short,rz_gs_en,rz_gs_headquarter,rz_gs_regist_addr,rz_gs_create_time,rz_gs_industry,rz_gs_site,rz_gs_intro,rz_gs_fax,rz_gs_tel,rz_gs_postcode,rz_gs_addr,rz_sj_list) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [item['rz_gs_detail'], item['rz_gs_logo'], item['rz_gs_name'], item['rz_gs_short'], item['rz_gs_en'],
			        item['rz_gs_headquarter'], item['rz_gs_regist_addr'], item['rz_gs_create_time'],
			        item['rz_gs_industry'], item['rz_gs_site'], item['rz_gs_intro'], item['rz_gs_fax'],
			        item['rz_gs_tel'], item['rz_gs_postcode'], item['rz_gs_addr'], item['rz_sj_list']
			        ]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['rz_gs_detail'])
