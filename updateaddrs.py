from common import *
def updateaddr():
	rent = Mydb()
	items = ['id', 'title', 'addr', 'area', 'city']
	table = 'rent58'
	updatelnglat = 0
	updateaddr = 0

	rent.select(table, items, None)
	records = rent.cur.fetchall()
	for record in records:
		id, title, addr, area, city = record
		condition = dict(id=id)
		taddr = title.split()[0]
		addr = area+addr
		for area in (taddr, addr):
			url = lnglat % (area, city)
			result = getapi(url)
			if result['status'] == 0:
				result = result['result']['location']
				lng = result['lng']
				lat = result['lat']
				rent.update(table, dict(lnglat=str(lng)+','+str(lat)), condition)
				updatelnglat += 1

				#update address
				url = location % (lng, lat)
				result = getapi(url)
				addr = result['result']['formatted_address']
				if addr: 
					rent.update(table, dict(addr=addr), condition)
					updateaddr += 1
				break
			elif result['status'] == 302:
				print(result['message'])
				exit()

	print('updated %s records of lng and lat, %s records of address' % (updatelnglat, updateaddr))

if __name__ == '__main__':
	updateaddr()