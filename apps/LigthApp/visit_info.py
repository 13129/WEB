from  .models import *
from django.db.models import F
from django.utils import timezone


import requests
from bs4 import BeautifulSoup



def change_info(request):
    #每一次访问总访问量+1
    try:
        count_nums=VisitNumber.objects.filter(id=1)##
        if count_nums.exists():
            count_nums=count_nums[0]
            count_nums.count=F('count')+1
        else:
            count_nums.count = 1
        count_nums.save()
        #记录每个IP的次数，ip地址
        if 'HTTP_X_FORWARDED_FOR' in request.META:#真实ip
            client_ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            client_ip = request.META['REMOTE_ADDR']
        #IP地址转换物理地址
        ip_exist=Touristfp.objects.filter(IP=str(client_ip))#查询是否有相同ip
        if ip_exist.exists():#有相同
            Tobj=ip_exist[0]
            Tobj.count=F('count')+1
            Tobj.start_time=timezone.now()

        else:#无相同
            url = "https://m.ip138.com/iplookup.asp?ip="
            kv = {"User-Agent": "Mozilla/5.0"}
            ip = str(client_ip)  # ip地址转换
            try:
                re_url = url + str(ip)
                r = requests.get(re_url, headers=kv)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text, 'lxml')
                result = soup.select('p[class="result"]')[0].string
                res = result.split("：")
            except:
                print("failed")
            Tobj=Touristfp(IP=client_ip,count=1,location=res[1])
        Tobj.save()

        #增加今日访问次数
        date=timezone.now().date()
        today=DayNumber.objects.filter(day=date)
        if today.exists():
            today =today[0]
            today.count =F('count')+ 1

        else:
            today=DayNumber()
            today.dayTime = date
            today.count = 1
        today.save()
    except Exception as err:
        print("")
