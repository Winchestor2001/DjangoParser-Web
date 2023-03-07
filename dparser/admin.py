from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Work

@admin.register(Work)
class WorkAdmin(TranslationAdmin):
    list_display = ['pk', 'title', 'date']
    list_filter = ('platform',)
    search_fields = ('date',)

