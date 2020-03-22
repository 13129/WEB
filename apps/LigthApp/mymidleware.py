from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,render
from .models import Touristfp,VisitNumber,DayNumber
import datetime
import time
from .visit_info import change_info
from django.utils import timezone
LIST_SITE=10#请求最大次数
RETRY_TIME=5#等待时间
LIST_CONT=3#访问间隔小于3秒清空

class Accessfrequency(MiddlewareMixin):

	def process_request(self,request):
		change_info(request)
		request_time = request.session.get("request_time", [])#如果有就不清空请求时间
		request_limit = request.session.get("request_limit",0)#请求限制

		now_time = time.time()

		if 'HTTP_X_FORWARDED_FOR' in request.META:  # 真实ip
			host_ip = request.META['HTTP_X_FORWARDED_FOR']
		else:
			host_ip = request.META['REMOTE_ADDR']

		ret=Touristfp.objects.filter(IP=host_ip).first()
		if not ret.is_lock:
		 	return HttpResponse("您的IP已经被封，有问题请联系管理员")
		if request_limit:
			time.sleep(1)
			visit_limit = now_time - request.session["request_time"][-1]#现在时间-session最新记录时间

			if visit_limit >= request_limit:#时间差>=1
				request_limit = 0#初始化
				visit_limit = 0#时间差初始化
				request.session["request_limit"] = request_limit
				request.session["request_time"] = []

			return HttpResponse("%d秒后重试" % (request_limit - visit_limit))

		#更新时间列表
		if request_time == []:
			request_time.append(now_time)
			request.session["request_time"] = request_time#更新列表
		else:
			request_time.append(now_time)
			request.session["request_time"] = request_time#更新列表

		# 10秒内访问超过VISIT_LIMIT次,则对其访问进行限制
		if len(request_time) >= LIST_SITE:#大于20时限制

			if request_time[0] - request_time[-1] <= LIST_SITE:#时间差小于20
				request.session["request_limit"] = RETRY_TIME#10
				return HttpResponse("访问过快,%d秒后重试" % (RETRY_TIME))#限制10秒
			else:
				request_time = []
				request.session["request_time"] = request_time#初始化session

		else:
			if len(request_time)>2:
				if request_time[-1]-request_time[-2] > LIST_CONT  :
					request_time =[]
					request.session['request_time']=request_time#初始化

