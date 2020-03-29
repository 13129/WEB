from django import template
from datetime import  *


#自定义过滤器转换中文，0000年00月00日 星期几
register = template.Library()
@register.filter
def chinese_time_now(value):
    def add(data):
        foo = range(1, 8)
        num = [str(x) for x in foo]
        week = dict(zip(num, '一二三四五六七'))
        data=str(data)
        for index, key in enumerate(week):
            if data == key:
                data = week[key]
                return data
    if isinstance(value,datetime):
        return "{}年{}月{}日 星期{}".format(value.year,value.month,value.day, add(value.now().isoweekday()))
    else:
        return value
#自定义过滤器---模型choices显示第二个值
@register.filter(name='displayName')
def displayName(value,arg):
    return eval('value.get_'+arg+'_display()')

