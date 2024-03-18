from django.urls import path
from company.views import *



# 企业端路由
urlpatterns = [
    path('', index),  # 企业首页
    path('company/', company_update),  # 企业信息修改
    path('photo/', photo_update),  # 企业图片修改
    path('center/', company),  # 企业信息
    path('login/', Login),  # 登录
    path('logout/', Logout),  # 注销登录
    path('register/', Register),  # 注册

    path('job/', job),  # 招聘信息
    path('job/insert/', job_insert),
    path('job/delete/<int:id>/', job_delete),
    path('job/update/<int:id>/', job_update),
    path('search/', search),
    path('submit_number/', submit_number),  # 排行
    path('earliest_release/', earliest_release),  # 最新发布


    path('interview/', interview),  # 面试邀请
    path('interview/<int:id>/', interview_start),  # 面试邀请
    path('interview/time/<int:id>/', interview_time),  # 面试时间约定

    path('send/', send),  # 简历投递
    path('send/<int:id>/', send_check),  # 简历查看
    path('send/<int:id>/<int:status>/', send_one),  # 邀面试/不合适

]
