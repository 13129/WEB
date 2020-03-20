from django.contrib import admin
from .models import Category, Tag, Blog, Banner, Tui


admin.site.site_header = 'Django管理后台'
admin.site.site_title = 'DjangoBLOG'


# Objects   模型类名

class TuiAdmin (admin.ModelAdmin):
	list_display = ('name',)


class BannerAdmin (admin.ModelAdmin):
	list_display = ('text_info','img','link_url','is_active')
	list_editable = [ 'link_url', 'is_active']
	list_display_links = ['text_info',]


class CategoryAdmin (admin.ModelAdmin):
	# def save_model
	list_display = ('name',)
	show_detail_fileds = ['name']  # 可以显示的后台列表名
	refresh_times = [5, 10, 20, 30, 60, 90, 120]  # 设置自动刷新


class TagAdmin (admin.ModelAdmin):
	list_display = ('name',)
	show_detail_fileds = ['name']
	refresh_times = [5, 10, 20, 30, 60, 90, 120]


class BlogAdmin (admin.ModelAdmin):
	list_display = ('name', 'title', 'tui','content' ,'category', 'create_time', 'modify_time',
	                'click_nums')
	list_filter = ('name', 'create_time', 'modify_time', 'click_nums', 'category', 'tagss')
	search_fields = ('name', 'title')  # 搜索字段
	list_editable = ['title', 'content',] # 可更改字段
	date_hierarchy = 'create_time'

admin.site.register (Category, CategoryAdmin)
admin.site.register (Tag, TagAdmin)
admin.site.register (Blog, BlogAdmin)
admin.site.register (Banner, BannerAdmin)
admin.site.register (Tui, TuiAdmin)
