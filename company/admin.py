from django.contrib import admin
from company.models import Company, Type, Job, Send, Interview


# Register your models here.
class companyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'name', 'phone', 'mail', 'photo', 'address', 'info','status']
    list_display_links = ['id', 'username', 'password', 'name', 'phone', 'mail', 'photo', 'address', 'info','status']
    search_fields = ['username', 'name', 'phone', 'mail', 'address', 'info']
    readonly_fields = ['id']


class typeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    readonly_fields = ['id']


class jobAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'workcity', 'company', 'type', 'salary', 'education', 'experience', 'content', 'create']
    list_display_links = ['id', 'name', 'workcity', 'company', 'type', 'salary', 'education', 'experience', 'content',
                          'create']
    search_fields = ['name', 'workcity', 'company', 'type', 'salary', 'education', 'experience', 'content']
    readonly_fields = ['id']


class sendAdmin(admin.ModelAdmin):
    list_display = ['id', 'resume', 'job', 'create', 'status']
    list_display_links = ['id', 'resume', 'job', 'create', 'status']
    search_fields = ['resume', 'job', 'status']
    readonly_fields = ['id']


class interviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'resume', 'company', 'job', 'user_status', 'time', 'create', 'status']
    list_display_links = ['id', 'user', 'resume', 'company', 'job', 'user_status', 'time', 'create', 'status']
    search_fields = ['user', 'resume', 'company', 'job', 'user_status', 'status']
    readonly_fields = ['id']


admin.site.register(Company, companyAdmin)
admin.site.register(Type, typeAdmin)
admin.site.register(Job, jobAdmin)
admin.site.register(Send, sendAdmin)
admin.site.register(Interview, interviewAdmin)
admin.site.site_header = "校园招聘系统-管理系统"
admin.site.site_title = "校园招聘系统-管理系统"
admin.site.index_title = "你好，管理员！"
