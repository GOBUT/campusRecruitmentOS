import random
import string

from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from user.models import *
from company.models import *
from django.conf import settings
from datetime import datetime
from io import BytesIO
from whutils.captcha import veri_code
import os
# 招聘大数据相关包
import json

from django.http import HttpResponse
from rest_framework.views import APIView
from pyecharts import options as opts_s
from pyecharts.charts import Grid, Line, Scatter, Bar, Pie, WordCloud
from pyecharts.faker import Faker

import re # 正则表达式库
import jieba # 结巴分词



def video_view_tencent(request):
    # 视频
    return render(request, 'video_tencent.html')


def video_view_bilibili(request):
    # 视频
    return render(request, 'video_bilibili.html')


def video_view_schneider(request):
    # 视频
    return render(request, 'video_schneider.html')


def captcha_img(request):
    stream = BytesIO()
    img, code = veri_code()
    img.save(stream, 'PNG')
    request.session['check_code'] = code
    return HttpResponse(stream.getvalue())


def index(request):
    """首页"""
    type = Type.objects.all()
    if request.method == 'GET':
        return render(request, 'index.html', {'type': type})
    if request.method == 'POST':
        kw = request.POST.get('kw')
        choice = request.POST.get('choice')
        if choice == 'company':
            jobs = Job.objects.filter(company__name__contains=kw)
        else:
            jobs = Job.objects.filter(name__contains=kw)
        # return render(request, 'user/job.html', {'lists': jobs, 'types': type})
        paginator = Paginator(jobs, 10)  # 对所有数据进行分页
        page_range = paginator.page_range  # 页码数列表
        page_page_sum = paginator.num_pages  # 页码数
        page_data_sum = paginator.count  # 总数数

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)
        return render(request, 'user/job.html', locals())

def all(request):
    jobs = Job.objects.all()
    paginator = Paginator(jobs, 10)  # 对所有数据进行分页
    page_range = paginator.page_range  # 页码数列表
    page_page_sum = paginator.num_pages  # 页码数
    page_data_sum = paginator.count  # 总数数

    try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
        current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
        current_page = paginator.page(current_page_num)  # 拿哪一页

        if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
            if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                current_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
            else:
                current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
        else:
            page_range = paginator.page_range  # 小于10页就显示所有页数

    except Exception as e:
        current_page_num = 1  # 随便乱传取第一页
        current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
        current_range = range(1, 12)
    return render(request, 'user/job.html', locals())

def type_id(request, id):
    jobs = Job.objects.filter(type_id=id)
    return render(request, 'user/job.html', {'lists': jobs})


def search(request):
    if request.method == 'GET':
        key_word= request.GET.get('key_word')
        ctype = int(request.GET.get('ctype'))
        type_value = request.GET.get('type')
        if ctype == 1:
            jobs=company_search(key_word)
        elif ctype == 2:
            jobs=salary_search(key_word)
        else:
            jobs = Job.objects.filter(type_id=type_value)
        paginator = Paginator(jobs, 10)  # 对所有数据进行分页
        page_range = paginator.page_range  # 页码数列表
        page_page_sum = paginator.num_pages  # 页码数
        page_data_sum = paginator.count  # 总数数

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)
        return render(request, 'user/job.html', locals())

    if request.method == 'POST':
        types = Type.objects.all()
        jobs = Job.objects.all()
        kw = request.POST.get('kw')
        type = request.POST.get('type')
        row = request.POST.get('row')
        if type != 'all':
            flag = 1
            ctype = 3
            jobs = jobs.filter(type_id=type)
        if kw:
            if row == 'company':
                flag = 1
                ctype = 1
                jobs = company_search(kw)
            elif row == 'salary':
                flag = 1
                ctype = 2
                jobs = salary_search(kw)
        # return render(request, 'user/job.html', {'lists': jobs, 'types': types, 'type': type})

        paginator = Paginator(jobs, 10)  # 对所有数据进行分页
        page_range = paginator.page_range  # 页码数列表
        page_page_sum = paginator.num_pages  # 页码数
        page_data_sum = paginator.count  # 总数数

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)

        return render(request, 'user/job.html', locals())

def company_search(kw):
    flag = 1
    jobs = Job.objects.filter(company__name__icontains=kw)
    return jobs

def salary_search(kw):
    flag = 1
    jobs = Job.objects.filter(salary_start__gte=int(kw))
    return jobs

def submit_number(request):
    flag = 4
    types = Type.objects.all()
    jobs = Job.objects.order_by('heat').reverse()
    paginator = Paginator(jobs, 10)  # 对所有数据进行分页
    page_range = paginator.page_range  # 页码数列表
    page_page_sum = paginator.num_pages  # 页码数
    page_data_sum = paginator.count  # 总数数

    try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
        current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
        current_page = paginator.page(current_page_num)  # 拿哪一页

        if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
            if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                current_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
            else:
                current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
        else:
            page_range = paginator.page_range  # 小于10页就显示所有页数

    except Exception as e:
        current_page_num = 1  # 随便乱传取第一页
        current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
        current_range = range(1, 12)

    return render(request, 'user/job.html', locals())


def latest_release(request):
    flag = 5
    types = Type.objects.all()
    jobs = Job.objects.order_by('create').reverse()
    paginator = Paginator(jobs, 10)  # 对所有数据进行分页
    page_range = paginator.page_range  # 页码数列表
    page_page_sum = paginator.num_pages  # 页码数
    page_data_sum = paginator.count  # 总数数

    try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
        current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
        current_page = paginator.page(current_page_num)  # 拿哪一页

        if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
            if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                current_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
            else:
                current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
        else:
            page_range = paginator.page_range  # 小于10页就显示所有页数

    except Exception as e:
        current_page_num = 1  # 随便乱传取第一页
        current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
        current_range = range(1, 12)

    return render(request, 'user/job.html', locals())


def education_equirements(request, academic):
    flag = 2
    types = Type.objects.all()
    if academic == '全部学历':
        jobs = Job.objects.all()
    else:
        jobs = Job.objects.filter(education__contains=academic)
    paginator = Paginator(jobs, 10)  # 对所有数据进行分页
    page_range = paginator.page_range  # 页码数列表
    page_page_sum = paginator.num_pages  # 页码数
    page_data_sum = paginator.count  # 总数数

    try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
        current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
        current_page = paginator.page(current_page_num)  # 拿哪一页

        if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
            if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                current_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
            else:
                current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
        else:
            page_range = paginator.page_range  # 小于10页就显示所有页数

    except Exception as e:
        current_page_num = 1  # 随便乱传取第一页
        current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
        current_range = range(1, 12)

    return render(request, 'user/job.html', locals())


def city_filter(request, city):
    flag = 3
    types = Type.objects.all()
    workcity = city
    if workcity == '全部':
        jobs = Job.objects.all()
    else:
        jobs = Job.objects.filter(workcity__contains=workcity)
    paginator = Paginator(jobs, 10)  # 对所有数据进行分页
    page_range = paginator.page_range  # 页码数列表
    page_page_sum = paginator.num_pages  # 页码数
    page_data_sum = paginator.count  # 总数数

    try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
        current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
        current_page = paginator.page(current_page_num)  # 拿哪一页

        if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
            if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                current_range = range(1, 11)
            elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
            else:
                current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
        else:
            page_range = paginator.page_range  # 小于10页就显示所有页数

    except Exception as e:
        current_page_num = 1  # 随便乱传取第一页
        current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
        current_range = range(1, 12)

    return render(request, 'user/job.html', locals())


def Register(request):
    '''注册'''

    if request.method == 'GET':
        '''显示注册页面'''
        return render(request, 'user/register.html')

    if request.method == 'POST':
        '''进行注册处理'''
        # 接收数据
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        check_code = request.POST.get('checkcode')
        last = request.POST.get('last')
        first = request.POST.get('first')

        if check_code and check_code.lower() != request.session.get('check_code').lower():
            errmsg = '验证码错误'
            return render(request, 'user/register.html', locals())

        if len(password) < 6:
            errmsg = '密码长度过短，建议6个或更多字符'
            return render(request, 'user/register.html', locals())

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            errmsg = '该邮箱已注册'
            return render(request, 'user/register.html', locals())

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username=email, password=password, first_name=first, last_name=last,
                                        email=email)
        # 自动激活用户
        user.is_active = 1
        # 保存
        user.save()
        # 返回应答, 跳转到登录页面
        return HttpResponse("<script>alert('注册成功！请登录！');window.location.href='/user/login/';</script>")


def forget_password(request):
    '''发送邮件找回密码 '''
    if request.method == "GET":
        return render(request, 'user/forget_password.html')

    if request.method == 'POST':
        check_code = request.POST.get('checkcode')
        if check_code and check_code.lower() != request.session.get('check_code').lower():
            errmsg = '验证码错误'
            return render(request, 'user/forget_password.html', locals())

        username = request.POST.get('username')
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            errmsg = '用户不存在'
            return render(request, 'user/forget_password.html', locals())
        if user:
            # 用户名已存在
            # 随机生成新密码
            random_password = gen_random_string(8)
            # 重置当前用户密码
            user = User.objects.get(username=username)
            user.set_password(random_password)
            user.save()
            send_mail(
                '【校园招聘系统】密码重置',  # 标题
                '尊敬的' + username + '同学，你好！\n您申请重置密码成功！\n您的新密码为：' + random_password + '\n\n请妥善保管新密码，尽快登录系统后在我的资料中进行修改！\n----校园招聘系统',
                # 内容
                settings.EMAIL_HOST_USER,  # 发送邮箱，已经在settings.py设置，直接导入
                [username],  # 目标邮箱 切记此处只能是列表或元祖
                fail_silently=True,  # 发送失败是否返回错误信息
            )
            # 返回应答, 跳转到登录页面
            return HttpResponse("<script>alert('重置成功，新密码请登录邮箱查看！');window.location.href='/user/login/';</script>")


def gen_random_string(length):
    # 随机生成字母和数字的位数
    numcount = random.randint(1, length - 1)
    lettercount = length - numcount
    # 随机抽样生成数字序列
    numlist = [random.choice(string.digits) for _ in range(numcount)]
    # 随机抽样生成字母序列
    letterlist = [random.choice(string.ascii_letters) for _ in range(lettercount)]
    # 合并字母数字序列
    alllist = numlist + letterlist
    # 乱序
    result = random.shuffle(alllist)
    # 生成目标结果字符串
    result = "".join([i for i in alllist])

    return result


def Login(request):
    '''登录'''

    if request.method == 'GET':
        return render(request, 'user/login.html')

    if request.method == 'POST':
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'user/login.html', {'errmsg': '请将必填项填写完整'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)
                return HttpResponse("<script>alert('登录成功！');window.location.href='/';</script>")
            else:
                # 用户未激活
                return render(request, 'user/login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'user/login.html', {'errmsg': '用户名或密码错误'})


def Logout(request):
    '''退出登录'''

    if request.method == 'GET':
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect('/')


@login_required
def pwdUpdate(request):
    '''用户密码修改'''

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'user/pwd_update.html')
        else:
            return redirect('/user/login/')

    if request.method == 'POST':
        if request.user.is_authenticated:
            # 获取当前用户
            user = request.user
            # 获取修改数据
            password = request.POST.get('pwd')
            cpassword = request.POST.get('cpwd')
            check_code = request.POST.get('checkcode')

            if check_code and check_code.lower() != request.session.get('check_code').lower():
                errmsg = '验证码错误'
                return render(request, 'user/register.html', locals())

            # 验证两次密码是否一致
            if password != cpassword:
                return render(request, 'user/pwd_update.html', {'errmsg': '两次输入的密码不一致'})
            # 修改当前用户密码
            user = User.objects.get(username=user)
            user.set_password(password)
            user.save()
            # 清除用户的session信息
            logout(request)
            return redirect('/user/login/')
        else:
            return redirect('/user/login/')


@login_required
def photoUpdate(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            info = User.objects.get(id=request.user.id)
            return render(request, 'user/photo_update.html', {'info': info})
        else:
            return redirect('/user/login/')

    if request.method == 'POST':
        info = User.objects.get(id=request.user.id)
        # 图片存储
        # 通过  FILES.get 获取 图片形式数据
        photo = request.FILES.get('photo')
        if photo and photo != info.photo:
            # 判断参数是否齐全
            if not photo:
                return render(request, 'photo_update.html', {'error': '请上传头像'})
            # 对文件名进行拼接防止加入静态文件夹时 出现重名的情况
            # 用添加时的当前时间进行一个动态的拼接
            fix = datetime.now().strftime('%Y%m%d%H%M%S%f') + 'user'

            # 上传图片
            # 对 我们settings中已经配置好的路径 把文件的名称进行存入
            img_path = os.path.join(settings.UPLOADUSER_DIRS, fix + photo.name)
            f = open(img_path, 'wb')
            for i in photo.chunks():
                f.write(i)
            f.close()

            # 图片路径存入数据库
            p = 'static/images/user/' + fix + photo.name
            info.photo = p
            info.save()
        return redirect('/user/')


@login_required
def usercenter(request):
    '''我的账户'''
    user = request.user
    info = User.objects.get(username=user)
    return render(request, 'user/user.html', {'info': info})


@login_required
def resume(request):
    '''我的简历'''
    user = request.user
    try:
        info = Resume.objects.get(user=user)
    except:
        info = Resume.objects.create(user=user, name=user.last_name + user.first_name, mail=user.email)
    return render(request, 'user/resume.html', {'info': info})


@login_required
def resume_update(request):
    '''简历填写'''
    user = request.user
    info = Resume.objects.get(user=user)
    if request.method == 'GET':
        return render(request, 'user/resume_update.html', {'info': info})
    if request.method == 'POST':
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        birth = request.POST.get('birth')
        registration = request.POST.get('registration')
        now = request.POST.get('now')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')
        job = request.POST.get('job')
        salary = request.POST.get('salary')
        education = request.POST.get('education')
        subject = request.POST.get('subject')
        language = request.POST.get('language')
        skill = request.POST.get('skill', '')
        certificates = request.POST.get('certificates', '')
        evaluation = request.POST.get('evaluation', '')

        if not all([name, sex, birth, registration, now, phone, mail, job, salary, education, subject]):
            return render(request, 'user/resume_update.html', {'info': info, 'errmsg': '个人信息、求职意向、教育经历、项目经历为必填项'})

        r = Resume.objects.filter(user=user)
        r.update(name=name, sex=sex, birth=birth, registration=registration, now=now, phone=phone, mail=mail, job=job,
                 salary=salary,
                 education=education, subject=subject, language=language, skill=skill, certificates=certificates,
                 evaluation=evaluation)
        # 图片存储
        # 通过  FILES.get 获取 图片形式数据
        photo = request.FILES.get('photo')
        if photo and photo != info.photo:
            # 判断参数是否齐全
            if not photo:
                return render(request, 'upload.html', {'error': '参数不全'})
            # 对文件名进行拼接防止加入静态文件夹时 出现重名的情况
            # 用添加时的当前时间进行一个动态的拼接
            fix = datetime.now().strftime('%Y%m%d%H%M%S%f') + '1'

            # 上传图片
            # 对 我们settings中已经配置好的路径 把文件的名称进行存入
            img_path = os.path.join(settings.UPLOADUSER_DIRS, fix + photo.name)
            f = open(img_path, 'wb')
            for i in photo.chunks():
                f.write(i)
            f.close()

            # 图片路径存入数据库
            p = 'static/images/user/' + fix + photo.name
            r.update(photo=p)

        file = request.FILES.get('file', None)
        if file and file != info.file:
            type = os.path.splitext(file.name)[-1]
            filename = r[0].name + '_' + datetime.now().strftime('%Y%m%d%H%M%S')
            destination = open(os.path.join(settings.UPLOADCV_DIRS, filename + type), 'wb+')
            for chunk in file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            r.update(file='resume/' + filename + type)

        return redirect('/user/resume/')


def job(request):
    if request.method == 'GET':
        types = Type.objects.all()
        jobs = Job.objects.all()
        paginator = Paginator(jobs, 10)  # 对所有数据进行分页
        page_range = paginator.page_range  # 页码数列表
        page_page_sum = paginator.num_pages  # 页码数
        page_data_sum = paginator.count  # 总数数

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)
        return render(request, 'user/job.html', locals())

    if request.method == 'POST':
        types = Type.objects.all()
        jobs = Job.objects.all()
        kw = request.POST.get('kw')
        type = request.POST.get('type')
        row = request.POST.get('row')
        education_need = request.POST.get('education_need')
        workcity = request.POST.get('work_city')
        if type != 'all':
            jobs = jobs.filter(type_id=type)
        if kw:
            if row == 'company':
                flag = 1
                ctype = 1
                jobs = company_search(kw)
            elif row == 'salary':
                flag = 1
                ctype = 2
                jobs = salary_search(kw)
        # return render(request, 'user/job.html', {'lists': jobs, 'types': types, 'type': type})

        paginator = Paginator(jobs, 10)  # 对所有数据进行分页
        page_range = paginator.page_range  # 页码数列表
        page_page_sum = paginator.num_pages  # 页码数
        page_data_sum = paginator.count  # 总数数

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)

        return render(request, 'user/job.html', locals())


# def job_index(request,id):
#     types = Job.objects.get(id=id)
#     jobs = Job.objects.all()
#     if request.method == 'GET':
#         return render(request, 'user/job.html', {'lists': jobs, 'types': types})


def job_detail(request, id):
    # 获取IP地址
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    # 设定 ip地址加上职位信息id组成唯一的一个值
    ip_id = ip + str(id)
    # 读取cache中存储的值
    online_ip_id = cache.get('online_ip_id', [])
    # 判断 chache中是否包含 ip_id
    if ip_id not in online_ip_id:
        online_ip_id.append(ip_id)
        cache.set("online_ip_id", online_ip_id, 60 * 60)  # 将新的online_ip_id存入到cache中 并设定时间为60分钟  写成1*60 为了好看易读
        print(cache.get('online_ip_id', []))
        pv_new = Job.objects.get(id=id)
        Job.objects.filter(id=id).update(pv=pv_new.pv + 1)

    job = Job.objects.get(id=id)
    return render(request, 'user/job_detail.html', {'job': job})


def data(request):
    # 招聘大数据
    return render(request, 'user/data.html')


def company(request):
    c = Company.objects.all()
    return render(request, 'user/company.html', {'lists': c})


def company_detial(request, id):
    c = Company.objects.get(id=id)
    lists = Job.objects.filter(company_id=id)
    return render(request, 'user/company_detail.html', {'c': c, 'lists': lists, 'count': len(lists)})


@login_required
def send(request):
    user = request.user
    s = Send.objects.filter(resume__user=user)
    return render(request, 'user/send.html', {'lists': s})


@login_required
def send_one(request, id):
    user = request.user
    uid = user.id
    if not user.status:
        return render(request, 'no_pr.html')
    if Send.objects.all().exists() is False:
        try:
            r = Resume.objects.get(user=user)
        except:
            return redirect('/user/resume/')
        Send.objects.create(resume=r, job_id=id, uid_id=uid)
        heat_new = Job.objects.get(id=id)
        Job.objects.filter(id=id).update(heat=heat_new.heat + 1)
        return redirect('/user/send/')
    if Send.objects.filter(uid_id=uid).exists() is True:
        if Send.objects.filter(job_id=id).exists():
            return HttpResponse("<script>alert('你已经申请过该职位！');window.location.href='/user/send/';</script>")
    try:
        r = Resume.objects.get(user=user)
    except:
        return redirect('/user/resume/')
    Send.objects.create(resume=r, job_id=id, uid_id=uid)
    heat_new = Job.objects.get(id=id)
    Job.objects.filter(id=id).update(heat=heat_new.heat + 1)
    return redirect('/user/send/')


@login_required
def interview(request):
    iw = Interview.objects.filter(user=request.user)
    now = datetime.now()
    for i in iw:
        end = datetime.strptime(i.time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        if end <= now and i.status == 1 and i.user_status == 2:
            i.time = end
    return render(request, 'user/interview.html', {'lists': iw, 'now': now})


@login_required
def interview_update(request, id, status):
    s = Interview.objects.filter(id=id)
    s.update(user_status=status)
    return redirect('/user/interview/')


def online_interview(request, id):
    s = Interview.objects.filter(id=id)
    print(s)
    return render(request, 'user/online_interview.html', {'lists': s})


# 大数据视图代码部分
# def response_as_json(data):
#     json_str = json.dumps(data)
#     response = HttpResponse(
#         json_str,
#         content_type="application/json",
#     )
#     response["Access-Control-Allow-Origin"] = "*"
#     return response
#
#
# def json_response(data, code=200):
#     data = {
#         "code": code,
#         "msg": "success",
#         "data": data,
#     }
#     return response_as_json(data)
#
#
# def json_error(error_string="error", code=500, **kwargs):
#     data = {
#         "code": code,
#         "msg": error_string,
#         "data": {}
#     }
#     data.update(kwargs)
#     return response_as_json(data)
#
#
# JsonResponse = json_response
# JsonError = json_error
#
# jobs = Job.objects.order_by('pv').reverse()
# name = [i.name for i in jobs]
# x = [i.pv for i in jobs]
# y = [i.heat for i in jobs]
#
# bar = (
#     Bar()
#         .add_xaxis(name)
#         .add_yaxis("访问量", x)
#         .add_yaxis("投递数", y)
#         .set_global_opts(
#         title_opts=opts.TitleOpts(title="访问、投递数"),
#         legend_opts=opts.LegendOpts(pos_left="20%"),
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
#         datazoom_opts=opts.DataZoomOpts(type_="inside")
#     )
# )

# scatter = (
#     Scatter()
#     .add_xaxis(Faker.choose())
#     .add_yaxis("商家A", Faker.values())
#     .add_yaxis("商家B", Faker.values())
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="Grid-Scatter", pos_right="5%"),
#         legend_opts=opts.LegendOpts(pos_right="25%"),
#     )
# )
# line2 = (
#     Line()
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .set_global_opts(
#         title_opts=opts.TitleOpts(title="Grid-Line", pos_right="10%"),
#         legend_opts=opts.LegendOpts(pos_right="35%")
#     )
# )


# def grid_table():
#     grid = (
#         Grid()
#             .add(chart=bar, grid_opts=opts.GridOpts(pos_bottom="60%", pos_right="55%"))
#             # .add(chart=pie, grid_opts=opts.GridOpts(pos_top="60%", width="38%"))
#             # .add(chart=scatter, grid_opts=opts.GridOpts(pos_left="55%", pos_bottom="60%"))
#             # .add(chart=line2, grid_opts=opts.GridOpts(pos_bottom="60%", pos_left="55%"))
#             # 获取全局 options，JSON 格式（JsCode 生成的函数带引号，在前后端分离传输数据时使用）
#             .dump_options_with_quotes()  # 官方解释：保留 JS 方法引号
#     )
#     return grid






# class ChartView(APIView):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(json.loads(grid_table()))
#
#
# class IndexView(APIView):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'user/data.html')

from pyecharts import options as opts_s
from pyecharts.charts import  Page, Pie
from pyecharts.faker import Faker
# jobs = Job.objects.order_by('pv').reverse()
# name = [i.name for i in jobs]
# x = [i.pv for i in jobs]
# y = [i.heat for i in jobs]

def pie_rosetype() -> Pie:
    jobs = Job.objects.all()
    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0
    for i in jobs:
        if i.type_id == 1:
            v1 += 1
        if i.type_id == 2:
            v2 += 1
        if i.type_id == 3:
            v3 += 1
        if i.type_id == 4:
            v4 += 1
    job_name = ['技术类','产品类','设计类','营销类']
    job_value = [v1,v2,v3,v4]

    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(job_name, job_value)],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts_s.LabelOpts(is_show=False),
        )
        .add(
            "",
            [list(z) for z in zip(job_name, job_value)],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
        .set_global_opts(title_opts=opts_s.TitleOpts(title="不同招聘类型数量图"))
    )
    return c

from pyecharts.charts import WordCloud








def page_simple_layout():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # bar_datazoom_slider(),
        # line_markpoint(),
        pie_rosetype(),
        # grid_mutil_yaxis(),
        # liquid_data_precision(),
        # table_base(),
    )
    page.render("templates/user/data_detail.html")


def data_btn(request):
    page_simple_layout()
    data = [
        ("校园招聘", "999"),
        ("招聘", "888"),
        ("技术", "777"),
        ("软件工程", "688"),
        ("计算机科学与技术", "588"),
        ("网络工程", "516"),
        ("腾讯", "515"),
        ("华为", "483"),
        ("房地产管理", "462"),
        ("城乡建设", "449"),
        ("社会保障与福利", "429"),
        ("社会保障", "407"),
        ("文体与教育管理", "406"),
        ("公共安全", "406"),
        ("公交运输管理", "386"),
        ("出租车运营管理", "385"),
        ("供热管理", "375"),
        ("市容环卫", "355"),
        ("自然资源管理", "355"),
        ("粉尘污染", "335"),
        ("噪声污染", "324"),
        ("土地资源管理", "304"),
        ("物业服务与管理", "304"),
        ("医疗卫生", "284"),
        ("粉煤灰污染", "284"),
        ("占道", "284"),
        ("供热发展", "254"),
        ("农村土地规划管理", "254"),
        ("生活噪音", "253"),
        ("供热单位影响", "253"),
        ("城市供电", "223"),
        ("房屋质量与安全", "223"),
        ("大气污染", "223"),
        ("房屋安全", "223"),
        ("文化活动", "223"),
        ("拆迁管理", "223"),
        ("公共设施", "223"),
        ("供气质量", "223"),
        ("供电管理", "223"),
        ("燃气管理", "152"),
        ("教育管理", "152"),
        ("医疗纠纷", "152"),
        ("执法监督", "152"),
        ("设备安全", "152"),
        ("政务建设", "152"),
        ("县区、开发区", "152"),
        ("宏观经济", "152"),
        ("教育管理", "112"),
        ("社会保障", "112"),
        ("生活用水管理", "112"),
        ("物业服务与管理", "112"),
        ("分类列表", "112"),
        ("农业生产", "112"),
        ("二次供水问题", "112"),
        ("城市公共设施", "92"),
        ("拆迁政策咨询", "92"),
        ("物业服务", "92"),
        ("物业管理", "92"),
        ("社会保障保险管理", "92"),
        ("低保管理", "92"),
        ("文娱市场管理", "72"),
        ("城市交通秩序管理", "72"),
        ("执法争议", "72"),
        ("商业烟尘污染", "72"),
        ("占道堆放", "71"),
        ("地上设施", "71"),
        ("水质", "71"),
        ("无水", "71"),
        ("供热单位影响", "71"),
        ("人行道管理", "71"),
        ("主网原因", "71"),
        ("集中供热", "71"),
        ("客运管理", "71"),
        ("国有公交（大巴）管理", "71"),
        ("工业粉尘污染", "71"),
        ("治安案件", "71"),
        ("压力容器安全", "71"),
        ("身份证管理", "71"),
        ("群众健身", "41"),
        ("工业排放污染", "41"),
        ("破坏森林资源", "41"),
        ("市场收费", "41"),
        ("生产资金", "41"),
        ("生产噪声", "41"),
        ("农村低保", "41"),
        ("劳动争议", "41"),
        ("劳动合同争议", "41"),
        ("劳动报酬与福利", "41"),
        ("医疗事故", "21"),
        ("停供", "21"),
        ("基础教育", "21"),
        ("职业教育", "21"),
        ("物业资质管理", "21"),
        ("拆迁补偿", "21"),
        ("设施维护", "21"),
        ("市场外溢", "11"),
        ("占道经营", "11"),
        ("树木管理", "11"),
        ("农村基础设施", "11"),
        ("无水", "11"),
        ("供气质量", "11"),
        ("停气", "11"),
        ("市政府工作部门（含部门管理机构、直属单位）", "11"),
        ("燃气管理", "11"),
        ("市容环卫", "11"),
        ("新闻传媒", "11"),
        ("人才招聘", "11"),
        ("市场环境", "11"),
        ("行政事业收费", "11"),
        ("食品安全与卫生", "11"),
        ("城市交通", "11"),
        ("房地产开发", "11"),
        ("房屋配套问题", "11"),
        ("物业服务", "11"),
        ("物业管理", "11"),
        ("占道", "11"),
        ("园林绿化", "11"),
        ("户籍管理及身份证", "11"),
        ("公交运输管理", "11"),
        ("公路（水路）交通", "11"),
        ("房屋与图纸不符", "11"),
        ("有线电视", "11"),
        ("社会治安", "11"),
        ("林业资源", "11"),
        ("其他行政事业收费", "11"),
        ("经营性收费", "11"),
        ("食品安全与卫生", "11"),
        ("体育活动", "11"),
        ("有线电视安装及调试维护", "11"),
        ("低保管理", "11"),
        ("劳动争议", "11"),
        ("社会福利及事务", "11"),
        ("一次供水问题", "11"),
    ]

    (
        WordCloud()
            .add(series_name="词云图", data_pair=data, word_size_range=[6, 66],width="100%",height="60%",pos_left="25%")
            .set_global_opts(

            title_opts=opts_s.TitleOpts(
                title="招聘大数据用户搜索词云", title_textstyle_opts=opts_s.TextStyleOpts(font_size=20)
            ),

            tooltip_opts=opts_s.TooltipOpts(is_show=False),
        )
            .render("templates/user/basic_wordcloud.html")
    )
    return render(request, 'user/data.html')

