from selenium import webdriver
import time
from lxml import html
import pymysql
import requests

headers = {	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Mobile Safari/537.36',

	}

# iK5K5VHGYVVXOFfi0fBocm5q
#7r5lNHNGvNja5KPYAfQRfTafFrVYZXrV
lnglat = 'http://api.map.baidu.com/geocoder/v2/?output=json&address=%s&city=%s&ak=iK5K5VHGYVVXOFfi0fBocm5q'
location = 'http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&pois=1&ak=iK5K5VHGYVVXOFfi0fBocm5q'

def getpage(url):
	for key, value in enumerate(headers):
		webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
	driver = webdriver.PhantomJS(executable_path='/home/lblue/bin/phantomjs')
	driver.get(url)
	time.sleep(1)
	with open('tmp.html','w') as f:
		f.write(driver.page_source)
	return html.fromstring(driver.page_source), driver.current_url

#return json format
def getpost(url, payload=None, headers=headers):
	r = requests.post(url, data=payload, headers=headers)
	return r.json()

def getapi(url):
	r = requests.get(url)
	return r.json()

class Mydb(object):
	def __init__(self, database='rent58', debug=False):
		self.conn = pymysql.connect(host='localhost', passwd = 'wdj654321', db = 'mysql', charset='utf8',port = 23306, user='wdj')
		self.cur = self.conn.cursor()
		self.cur.execute('USE %s' % database)
		self.debug = debug

	def insert(self, table, data):
		query = ''
		values = ''
		for v in data.values():
			values += "'"+str(v)+"'"+','
		values = values[:-1]
		columns = '`,`'.join(data.keys())
		columns = '`'+columns
		columns += '`'

		sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, values)
		if self.debug:
			print(sql)
		self.cur.execute(sql)
		self.conn.commit()

	def update(self, table, data, condition, logic='and'):
		pat = "`%s`='%s',"
		wpat = " `%s`='%s' %s"
		query = ''
		for k, v in data.items():
			query += pat % (k,v)
		query = query[:-1]
		where = ''
		for k, v in condition.items():
			where += wpat % (k, v, logic)
		where = where[:-1*len(logic)]
		sql = "UPDATE %s SET %s WHERE %s" % (table, query, where)
		if self.debug:
			print(sql)
		self.cur.execute(sql)
		self.conn.commit()

	def delete(self, table, condition, logic='and'):
		wpat = " `%s`='%s' %s"
		where = ''
		for k, v in condition.items():
			where += wpat % (k, v, logic)
		where = where[:-1*len(logic)]
		sql = 'DELETE FROM %s WHERE %s' % (table, where)
		if self.debug:
			print(sql)
		self.cur.execute(sql)
		self.conn.commit()

	def select(self, table, data, condition, logic='and'):
		wpat = " `%s`='%s' %s"
		columns = '`,`'.join(data)
		columns = '`'+columns
		columns += '`'
		where = ''
		if not condition:
			sql = 'SELECT %s FROM %s %s'
		else:
			sql = 'SELECT %s FROM %s WHERE %s'
			for k, v in condition.items():
				where += wpat % (k, v, logic)
			where = where[:-1*len(logic)]

		sql = sql % (columns, table, where)
		if self.debug:
			print(sql)
		self.cur.execute(sql)
		self.conn.commit()

	def truncate(self, table):
		sql = 'TRUNCATE %s' % table
		self.cur.execute(sql)
		self.conn.commit()