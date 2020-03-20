from django import template
from datetime import  *

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


