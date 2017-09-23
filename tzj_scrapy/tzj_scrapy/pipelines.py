# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):
	"""
	本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""

	def __init__(self):
		self.conn = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if spider.name == 'touzishijian':
		# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """insert into touzijie_touzishijian (detail_url, tz_sj_title, rz_comp_url, rz_comp_name, tz_jg_list, currency, money, invest_loop, invest_time, indus_list, invest_intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [
			item['detail_url'], item['tz_sj_title'], item['rz_comp_url'], item['rz_comp_name'], item['tz_jg_list'],
			item['currency'], item['money'], item['loop'], item['invest_time'], item['indus_list'],
			item['invest_intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['detail_url'])
		elif spider.name == 'detail':
			sql = """update weixin_base_info set feature=%s WHERE pub_name=%s"""
			args = (item["feature"], item["pub_name"])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			print(str(item['pub_name']))
