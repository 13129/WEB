from django.contrib import admin
from .models import Ligthapp, Touristfp, Link,Notice,VisitNumber,DayNumber

class VisitNumberAdmin(admin.ModelAdmin):
	list_display=('count',)
class DayNumberAdmin(admin.ModelAdmin):
	list_display=('day','count')

class NoticeAdmin(admin.ModelAdmin):
	list_display=('level','release_time','detail')

class TouristfpAdmin (admin.ModelAdmin):
	list_display = ('IP','location','start_time','count','is_lock')

class LigthappAdmin (admin.ModelAdmin):
	list_display = ('name', 'number', 'status')

class LinkAdmin (admin.ModelAdmin):
	list_display = ('name', 'linkurl', 'linkimg', 'add_time')
	search_fields = ('name', 'linkurl')

admin.site.register (DayNumber,DayNumberAdmin)
admin.site.register (VisitNumber,VisitNumberAdmin)
admin.site.register (Notice,NoticeAdmin)
admin.site.register (Link, LinkAdmin)
admin.site.register (Touristfp, TouristfpAdmin)
admin.site.register (Ligthapp, LigthappAdmin)
