from django.contrib import admin
from .models import Routine

class RoutineAdmin(admin.ModelAdmin):
    list_display = ('day', 'time_slot', 'course_code', 'course_name')
    list_filter = ('day', 'time_slot')
    search_fields = ('course_code', 'course_name')

admin.site.register(Routine, RoutineAdmin)