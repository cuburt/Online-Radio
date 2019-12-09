from django.contrib import admin
from .models import Cluster,Candidate, Position, Tabulation, News, News_category, Modules, Action_flag, Activity_Log, Programs, Products, Keyword, Landing_page, Alignment, Client, is_agency_represented,Info,Page,ContactJACK_message, Live_File, Content_Manager, Identification_Number
from tinymce.widgets import TinyMCE
from django.db import models

class NewsAdmin(admin.ModelAdmin):

    # fieldsets = [
    #     ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
    #     ("Content", {"fields": ["tutorial_content"]})
    # ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }

class InfoAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

# Register your models here.
admin.site.register(Tabulation)
admin.site.register(Cluster)
admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(News, NewsAdmin)
admin.site.register(News_category)
admin.site.register(Modules)
admin.site.register(Action_flag)
admin.site.register(Activity_Log)
admin.site.register(Programs)
admin.site.register(Products)
admin.site.register(Keyword)
admin.site.register(Landing_page)
admin.site.register(Alignment)
admin.site.register(Client)
admin.site.register(is_agency_represented)
admin.site.register(Info, InfoAdmin)
admin.site.register(Page)
admin.site.register(ContactJACK_message)
admin.site.register(Live_File)
admin.site.register(Content_Manager)
admin.site.register(Identification_Number)


