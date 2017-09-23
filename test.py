import pymysql

conn = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
                       charset='utf8'
                       , cursorclass=pymysql.cursors.SSCursor
                       )
cursor = conn.cursor()

sql = """insert into touzijie_touzishijian_copy(detail_url, tz_sj_title, rz_comp_url, rz_comp_name, tz_jg_list, currency,money,abc,invest_time,indus_list,invest_intro) VALUES ("111","22","3","不公开的投资者",
           # "[{'tz_jg_url': 'http://zdb.pedaily.cn/company/show12278/', 'tz_jg_name': '不公开的投资者'}, {'tz_jg_url': 'http://zdb.pedaily.cn/company/show9814/', 'tz_jg_name': '高榕资本'}]",
           'aaa',
           "RMB",
           "6千万",
           "A",
           "2017年09月22日",
           # "[{'indus_url': 'http://zdb.pedaily.cn/inv/h3362', 'indus_name': '金融'}]",
           'bbb',
           "2017年9月22日，高榕资本、不公开的投资者投资上海雷励投资管理有限公司6000万人民币。")"""

context = ("111",
           "22",
           "3",
           "不公开的投资者",
           # "[{'tz_jg_url': 'http://zdb.pedaily.cn/company/show12278/', 'tz_jg_name': '不公开的投资者'}, {'tz_jg_url': 'http://zdb.pedaily.cn/company/show9814/', 'tz_jg_name': '高榕资本'}]",
           'aaa',
           "RMB",
           "6千万",
           "A",
           "2017年09月22日",
           # "[{'indus_url': 'http://zdb.pedaily.cn/inv/h3362', 'indus_name': '金融'}]",
           'bbb',
           "2017年9月22日，高榕资本、不公开的投资者投资上海雷励投资管理有限公司6000万人民币。")

try:
	cursor.execute(sql)
	conn.commit()
finally:
	cursor.close()
	conn.close()
