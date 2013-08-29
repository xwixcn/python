"""" the admin site config"""
from django.contrib import admin
from verify.models import Case
from verify.models import IncludeResult
from verify.models import Job


class CaseAdmin(admin.ModelAdmin):
	list_display=("query","comparelist","addtime")

class IncludeResultAdmin(admin.ModelAdmin):
	list_display=("case","falseresult","jobid","linktowencai")
	list_filter=("case","falseresult","jobid")


class JobAdmin(admin.ModelAdmin):
	list_display=("id","totalnum","successnum","errornum","successnum","fail_cases","run_time",)

admin.site.register(Case,CaseAdmin)
admin.site.register(IncludeResult,IncludeResultAdmin)
admin.site.register(Job,JobAdmin)