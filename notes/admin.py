from django.contrib import admin
from .models import Note, Report

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'module_code', 'uploaded_by', 'upload_date', 'rating')
    list_filter = ('module_code', 'upload_date')
    search_fields = ('title', 'module_code', 'description')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('note', 'reported_by', 'report_date', 'resolved')
    list_filter = ('resolved', 'report_date')
    search_fields = ('note__title', 'reason')

admin.site.register(Note, NoteAdmin)
admin.site.register(Report, ReportAdmin)