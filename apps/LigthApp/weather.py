import requests
import json
from bs4 import BeautifulSoup
from datetime import *

def weath(address):
	rb=requests.get('http://wthrcdn.etouch.cn/weather_mini?city=%s'%(address))
	datas=json.loads(rb.text)
	datas=datas['data']['forecast'][0]
	return datas

def cleander():
	days=datetime.now().day
	url="https://wannianrili.51240.com/"
	kv={"User-Agent":"Mozilla/5.0"}
	res=requests.get(url,headers=kv)
	res.raise_for_status()
	res.encoding=res.apparent_encoding
	soup=BeautifulSoup(res.text,'lxml')
	soup=soup.find(id="wnrl_k_you_id_%s"%(days-1))
	cleand=[i.text for i in (soup.contents)[2:4]]
	return cleand
