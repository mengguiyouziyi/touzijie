import requests
from scrapy import Selector
from urllib.parse import urljoin

burl = "http://zdb.pedaily.cn"
lurl = "http://zdb.pedaily.cn/inv/"

headers = {
	'upgrade-insecure-requests': "1",
	'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	'referer': "http://zdb.pedaily.cn/inv/p1",
	'accept-encoding': "gzip, deflate",
	'accept-language': "zh-CN,zh;q=0.8",
	'cookie': "__uid=1818273228; BAIDU_SSP_lcr=https://www.baidu.com/link?url=zKfMujyv2RxSUtuTnbZMsCx6mSEVACw_mp3oL_9XBna&wd=&eqid=9b10a90700042e210000000359c24539; __utmt=1; jiathis_rdc=%7B%22http%3A//zdb.pedaily.cn/inv/show12525/%22%3A-1470910791%2C%22http%3A//zdb.pedaily.cn/company/show12283/%22%3A-1470883795%2C%22http%3A//zdb.pedaily.cn/enterprise/show32554%22%3A0%7C1506062811959%2C%22http%3A//zdb.pedaily.cn/company/show15613%22%3A%220%7C1506062835674%22%7D; ARRAffinity=197ae5372184c64aeca47f780a2e053f3a50366e2bda392cd4bfa3b38e39a929; Hm_lvt_25919c38fb62b67cfb40d17ce3348508=1505903948; Hm_lpvt_25919c38fb62b67cfb40d17ce3348508=1506063033; __utma=23980325.1982964119.1505903948.1505903948.1506062556.2; __utmb=23980325.19.10.1506062556; __utmc=23980325; __utmz=23980325.1505903948.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic",
	'cache-control': "no-cache",
	'postman-token': "385d961a-1a59-0fd0-76ed-a04a3a2e1b13"
}
tz_sj_dict = {}


def get_list(url):
	response = requests.request("GET", url, headers=headers)
	sel = Selector(text=response.text)

	urls = sel.xpath('//dt[@class="view"]/a/@href').extract()
	url_list = [urljoin(burl, x) for x in urls if urls]
	for u in url_list:
		tz_sj_dict['detail_url'] = u
		get_detail(u)

	next_url = sel.xpath('//a[@class="next"]/@href').extract_first()
	if next_url:
		get_list(next_url)


def get_detail(url):
	response = requests.request("GET", url, headers=headers)
	sel = Selector(text=response.text)
	tz_sj_title = sel.xpath('//div[@class="info"]/h1/text()').extract_first()
	rz_comp_url = sel.xpath('//li[@class="full"]/a[contains(@href, "enterprice")]/@href').extract_first()
	rz_comp_name = sel.xpath('//li[@class="full"]/a[contains(@href, "enterprice")]/text()').extract_first()
	tz_jg_tag = sel.xpath('//li[@class="full"]/a[contains(@href, "company")]')
	for tag in tz_jg_tag:
		tz_jg_url = tag.xpath('./@href').extract_first()
		tz_jg_name = tag.xpath('./text()').extract_first()
		tz_jg_info = {'tz_jg_url': tz_jg_url, 'tz_jg_name': tz_jg_name}
		tz_sj_dict.update('tz_jg_info', tz_jg_info)
