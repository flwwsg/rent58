from common import *
import requests
import time

def chkcode(url):
	baseurl = 'http://callback.58.com/firewall'
	resp, current_url = getpage(url)
	uuid = resp.xpath('//input[@id="uuid"]/@value')[0]
	namespace = resp.xpath('//input[@id="namespace"]/@value')[0]
	url = resp.xpath('//input[@id="url"]/@value')[0]
	ip = resp.xpath('//input[@id="ip"]/@value')[0]
	imgsrc = resp.xpath("//img[@id='verify_img']/@src")[0]
	imgsrc = imgsrc[2:]
	img = requests.get(baseurl+imgsrc, stream=True, allow_redirects=False)
	with open('code.jpg', 'wb') as f:
		for chunk in img.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
	verify_code = input('please input verify code named code.jpg in current folder: ')
	payload = {'uuid':uuid, 'namespace':namespace, 'url':url,'verify_code':verify_code}
	r = requests.post(current_url, data=payload, headers=headers)
	resp = r.json()
	if resp['code'] != 0:
		return chkcode(current_url)
	else: 
		return resp['msg']
