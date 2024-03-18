from django.conf.urls import url
from django.urls import path
from user.views import *


# 用户端路由
urlpatterns = [
    path('login/', Login),  # 登录
    path('logout/', Logout),  # 注销登录
    path('register/', Register),  # 注册
    path('forget_password/', forget_password),  # 忘记密码
    path('send/', send),  # 邮箱验证
    path('type/<int:id>/', type_id),  # 显示类型
    path('search/', search),  # 搜索
    path('all/', all),  # 全部
    path('submit_number/',submit_number),#排行
    path('latest_release/',latest_release),#最新发布
    path('education_equirements/<str:academic>/', education_equirements),  # 学历筛选
    path('city_filter/<str:city>/', city_filter),  # 城市筛选

    path('', usercenter),  # 用户中心
    path('password/', pwdUpdate),  # 用户密码修改
    path('photo/', photoUpdate),  # 用户头像修改
    path('resume/', resume),  # 我的简历
    path('resume/update/', resume_update),  # 简历填写

    path('job/', job),  # 招聘信息
    path('job/<int:id>/', job_detail),  # 招聘信息
    path('data/',data_btn),#招聘大数据
    # path('bar/', ChartView.as_view()),
    # url(r'^data/$', IndexView.as_view()),

    path('company/', company),  # 企业
    path('company/<int:id>/', company_detial),  # 企业
    path('send/', send),  # 简历投递
    path('send/<int:id>/', send_one),  # 简历投递
    path('interview/', interview),  # 面试邀请
    path('interview/<int:id>/<int:status>/', interview_update),  # 面试接受
    path('online_interview/<int:id>/', online_interview),  # 面试接受


    #宣讲会视频
    path('video_tencent',video_view_tencent),
    path('video_bilibili', video_view_bilibili),
    path('video_schneider', video_view_schneider),

]
