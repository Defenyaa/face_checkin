from django.contrib import admin
from class_checkin.models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

# class class_studentAdmin(admin.ModelAdmin):
#     list_display = ['sid', 'name', 'class_room', 'isroom']


class query_logAdmin(admin.ModelAdmin):
    list_display = ['date', 'class_room', 'picture', 'log']

admin.site.register(query_log, query_logAdmin)
# admin.site.register(class_student, class_studentAdmin)

@admin.register(class_student)
class PersonAdmin(ImportExportModelAdmin):
    pass