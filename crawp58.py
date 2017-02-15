from common import *
from handle_check_code import chkcode
from updateaddrs import updateaddr

url = 'http://sh.58.com/zufang/0'

def getitems(url):
	resp, current_url = getpage(url)
	infos = resp.xpath('//div[@class="content"]//ul[@class="listUl"]//li')
	titles, urls, addrs, money = list(), list(), list(), list()
	for info in infos:
		addr = info.xpath('div[@class="des"]//p[@class="add"]//a//text()')
		geren = info.xpath('div[@class="des"]//p[@class="geren"]//text()')
		if not geren:
			continue
		title = info.xpath('div[@class="des"]//h2//text()')[1].strip()
		url = info.xpath('div[@class="des"]//h2//a/@href')[0].strip()
		money2 = info.xpath('div[@class="listliright"]//div[@class="money"]//b//text()')[0]
		titles.append(title)
		urls.append(url)
		addrs.append(addr)
		money.append(money2)

	nextlink = resp.xpath('//div[@class="pager"]//a[@class="next"]/@href')
	if nextlink:
		nextlink = nextlink[0].strip()
	print(nextlink)
	# print(len(titles) == len(urls), len(titles) == len(money))
	# print(addrs, nextlink)
	return titles, urls, addrs, money, nextlink

def geturl(url):
	resp, current_url = getpage(url)
	infos = resp.xpath('//div[@class="content"]//ul[@class="listUl"]//li')
	if not infos:
		url = chkcode(current_url)
		url = 'http://'+url
	return url

if __name__ == '__main__':
	db = Mydb()
	table = 'rent58'
	db.truncate(table)
	while url:
		url = geturl(url)
		titles, urls, addrs, money, nextlink = getitems(url)
		for url, title, cmoney, (area, addr) in zip(urls, titles, money, addrs):
			if cmoney == '面议':
				cmoney = 1
			db.select(table, ['id'], dict(title=title, url=url))
			if not db.cur.rowcount:
				db.insert(table,dict(url=url, title=title, money=cmoney, area=area, addr=addr))
			else:
				db.update(table, dict(money=cmoney, area=area, addr=addr), dict(title=title, url=url))
		url = nextlink

	print('Updating longitude and latitude.')
	updateaddr()
	db.cur.close()
	db.conn.close()


