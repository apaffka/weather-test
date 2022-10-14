from django.contrib import admin

from .models import Loging


class LogingAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'date',
                    'city',
                    'latitude',
                    'longitude',
                    'status')
    search_fields = ('date', 'cuty')
    list_filter = ('date',)
    empty_value_display = '-пусто-'


admin.site.register(Loging, LogingAdmin)
