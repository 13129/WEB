from django import template

register = template.Library()


# @register.filter
# def help_text(value, arg):
#     return value._meta.get_field(arg).help_text
@register.filter(name='get')
def get(d, k):
    return d[str(k)]