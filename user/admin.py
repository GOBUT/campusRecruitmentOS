from django.contrib import admin
from user.models import User, Resume


# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'email', 'is_superuser', 'status']
    list_display_links = ['id', 'username', 'password', 'email', 'is_superuser', 'status']
    search_fields = ['username']
    fields = ['id', 'username', 'password', 'first_name','last_name','email', 'is_superuser', 'status']
    readonly_fields = ['id']


class resumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'sex', 'birth', 'registration', 'now', 'phone', 'mail', 'photo', 'job', 'salary', 'education',
                    'subject']
    # list_display_links = ['id', 'username', 'password', 'is_superuser', 'email']
    search_fields = ['name', 'sex', 'registration', 'now', 'phone', 'mail', 'job', 'salary', 'edu', 'subject']
    readonly_fields = ['id']


admin.site.register(User, userAdmin)
admin.site.register(Resume, resumeAdmin)
admin.site.site_header = "校园招聘系统-后台系统"
admin.site.site_title = "校园招聘系统-后台系统"
admin.site.index_title = "你好，管理员！"
