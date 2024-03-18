from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from company.models import *
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import os


# Create your views here.

def index(request):
    """首页"""
    company = request.session.get('company', None)
    if not company:
        # 企业未登录
        return redirect('/company/login/')
    type = Type.objects.all()
    if request.method == 'GET':
        return render(request, 'company/index.html', {'type': type})
    if request.method == 'POST':
        kw = request.POST.get('kw')
        choice = request.POST.get('choice')
        if choice == 'company':
            jobs = Job.objects.filter(company__name__contains=kw)
        else:
            jobs = Job.objects.filter(name__contains=kw)
        return render(request, 'company/job.html', {'lists': jobs})


def Login(request):
    '''登录'''
    if request.method == 'GET':
        return render(request, 'company/login.html')
    if request.method == 'POST':
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        check_code = request.POST.get('checkcode')

        # 校验数据
        if check_code and check_code.lower() != request.session.get('check_code').lower():
            errmsg = '验证码错误'
            return render(request, 'user/login.html', locals())

        # 业务处理:登录校验
        try:
            company = Company.objects.get(username=username, password=password)
            # 企业名密码正确
            # 记录企业的登录状态
            request.session['company'] = company.name
            request.session['id'] = company.id
            if company.photo:
                request.session['img'] = company.photo.url
            return HttpResponse("<script>alert('登录成功！');window.location.href='/company/';</script>")
        except:
            # 企业名密码不正确
            return render(request, 'company/login.html', {'errmsg': '企业名或密码错误'})


def Register(request):
    '''注册'''

    if request.method == 'GET':
        '''显示注册页面'''
        return render(request, 'company/register.html')

    if request.method == 'POST':
        '''进行注册处理'''
        # 接收数据
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        check_code = request.POST.get('checkcode')
        name = request.POST.get('name')

        # 校验数据
        if check_code and check_code.lower() != request.session.get('check_code').lower():
            errmsg = '验证码错误'
            return render(request, 'user/register.html', locals())
        # 校验企业名是否重复
        try:
            user = Company.objects.get(username=email)
        except Company.DoesNotExist:
            # 企业名不存在
            user = None
        if user:
            # 企业名已存在
            return render(request, 'company/register.html', {'errmsg': '该邮箱已注册'})

        # 进行业务处理: 进行企业注册
        Company.objects.create(username=email, password=password, name=name, mail=email)
        # 返回应答, 跳转到登录页面
        return HttpResponse("<script>alert('注册成功！请登录！');window.location.href='/company/login/';</script>")


def Logout(request):
    '''退出登录'''
    if request.method == 'GET':
        # 清除企业的session信息
        if request.session.get('img',None):
            del request.session['img']
        del request.session['id']
        del request.session['company']
        # 跳转到首页
        return redirect('/company/login/')


def job(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    # jobs = Job.objects.all()
    jobs = Job.objects.filter(company_id=cid)
    return render(request, 'company/job.html', {'lists': jobs})


def job_insert(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    company = Company.objects.get(id=cid)
    if not company.status:
        return render(request, 'company/no_pr.html')
    types = Type.objects.all()
    if request.method == 'GET':
        return render(request, 'company/job_insert.html', {'types': types})
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('workcity')
        type = request.POST.get('type')
        salary_start = request.POST.get('salary_start')
        salary_end = request.POST.get('salary_end')
        if salary_start and salary_end in '0':
            salary = "面议"
        elif salary_start and salary_end not in '0':
            if int(salary_start) > int(salary_end):
                return render(request, 'company/job_insert.html', {'errmsg': '请填写正确的薪资！', 'types': types})
            else:
                salary = str(salary_start) + '-' + str(salary_end)
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        content = request.POST.get('content')
        if not all([name, city, type, content, experience, education, salary_start,salary_end]):
            return render(request, 'company/job_insert.html', {'errmsg': '请将信息填写完整', 'types': types})
        Job.objects.create(name=name, workcity=city, type_id=type, salary_start=salary_start,salary_end=salary_end,salary=salary, education=education, experience=experience,
                           content=content,
                           company_id=request.session.get('id'))
        return redirect('/company/job/')


def job_update(request, id):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    company = Company.objects.get(id=cid)
    if not company.status:
        return render(request, 'company/no_pr.html')
    info = Job.objects.get(id=id)
    types = Type.objects.all()
    if request.method == 'GET':
        return render(request, 'company/job_update.html', {'id': id, 'info': info, 'types': types})
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('workcity')
        type = request.POST.get('type')
        # salary = request.POST.get('salary')
        salary_start = request.POST.get('salary_start')
        salary_end = request.POST.get('salary_end')
        if salary_start and salary_end in '0':
            salary = "面议"
        elif salary_start and salary_end not in '0':
            if int(salary_start) > int(salary_end):
                return render(request, 'company/job_update.html', {'errmsg': '请填写正确的薪资！', 'types': types})
            else:
                salary = str(salary_start) + '-' +str(salary_end)
        education = request.POST.get('education')
        print(education)
        experience = request.POST.get('experience')
        content = request.POST.get('content')
        if not all([name, city, type, content, experience, education, salary_start,salary_end]):
            return render(request, 'company/job_update.html', {'errmsg': '请将信息填写完整', 'types': types})
        Job.objects.filter(id=id).update(name=name, workcity=city, type_id=type, salary_start=salary_start,salary_end=salary_end,salary=salary, education=education,experience=experience,content=content)
        return redirect('/company/job/')


def job_delete(request, id):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    company = Company.objects.get(id=cid)
    if not company.status:
        return render(request, 'company/no_pr.html')
    if request.method == "GET":
        Job.objects.filter(id=id).delete()
        return redirect('/company/job/')


def send(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    c_id = request.session.get('id')
    s = Send.objects.filter(job__company__id=c_id)
    return render(request, 'company/send.html', {'lists': s})


def send_check(request, id):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    s = Send.objects.filter(id=id)
    if s[0].status == 1:
        s.update(status=2)
    return render(request, 'company/send_check.html',
                  {'job': s[0].job, 'info': s[0].resume, 'id': id, 'status': s[0].status})


def send_one(request, id, status):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    s = Send.objects.filter(id=id)
    s.update(status=status)
    if status == 4:
        return redirect('/company/send/')
    if status == 3:
        i = Interview.objects.create(user=s[0].resume.user, resume=s[0].resume, company=s[0].job.company, job=s[0].job)
        return render(request, 'company/interview_time.html', {'iw': i})


def interview_time(request, id):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    iw = Interview.objects.filter(id=id)
    date = request.POST.get('date')
    time = request.POST.get('time')
    meeting = request.POST.get('meeting')
    iw.update(meetingid=meeting)
    iw.update(time=date + ' ' + time)
    send_mail_to(iw[0])
    return redirect('/company/send/')


def interview(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    iw = Interview.objects.filter(company_id=request.session.get('id'))
    now = datetime.now()
    for i in iw:
        end = datetime.strptime(i.time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        if end <= now and i.status == 1 and i.user_status == 2:
            i.time = end
    return render(request, 'company/interview.html', {'lists': iw, 'now': now})


def interview_start(request, id):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    if request.method == 'GET':
        i = Interview.objects.get(id=id)
        return render(request, 'company/interview_start.html', {'iw': i, 'info': i.resume})
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == '1':
            Interview.objects.filter(id=id).update(status=3)
        else:
            Interview.objects.filter(id=id).update(status=2)
    return redirect('/company/interview/')


def company_update(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    info = Company.objects.get(id=request.session.get('id'))
    if request.method == 'GET':
        return render(request, 'company/company_update.html', {'info': info})
    if request.method == 'POST':
        name = request.POST.get('name')
        io = request.POST.get('info')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')
        address = request.POST.get('address')

        if not all([name, phone, mail, job, io, address]):
            return render(request, 'company/company_update.html', {'info': info, 'errmsg': '个人信息、求职意向、教育经历、项目经历为必填项'})

        Company.objects.filter(id=request.session.get('id')).update(name=name, phone=phone, mail=mail,
                                                                    address=address, info=io)
        return redirect('/company/company/')


def photo_update(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    r = Company.objects.filter(id=request.session.get('id'))
    # 图片存储
    # 通过  FILES.get 获取 图片形式数据
    photo = request.FILES.get('photo')
    # 对文件名进行拼接防止加入静态文件夹时 出现重名的情况
    # 用添加时的当前时间进行一个动态的拼接
    fix = datetime.now().strftime('%Y%m%d%H%M%S%f') + '1'

    # 上传图片
    # 对 我们settings中已经配置好的路径 把文件的名称进行存入
    img_path = os.path.join(settings.UPLOADCOM_DIRS, fix + photo.name)
    f = open(img_path, 'wb')
    for i in photo.chunks():
        f.write(i)
    f.close()

    # 图片路径存入数据库
    p = 'static/images/company/' + fix + photo.name
    r.update(photo=p)
    request.session['img'] = r.first().photo.url
    return redirect('/company/company/')


def company(request):
    cid = request.session.get('id',None)
    if not cid:
        return redirect('/company/login/')
    c = Company.objects.get(id=request.session.get('id'))
    return render(request, 'company/company.html', {'c': c})



def send_mail_to(info):
    send_mail(
        '【校园招聘系统】面试邀请',  #
        '恭喜您收到一份面试邀请！\n您已通过简历筛选，' + info.company.name + ' 邀请您进行面试。\n\n申请职位：' + info.job.name + '\n所属企业：' + info.company.name + '\n面试时间：' + str(info.time) + ' \n\n请回到网站页面，接受面试并使用腾讯会议（会议号：' +info.meetingid +'）进入继续您的操作。\n——校园招聘系统',  # 内容
        settings.EMAIL_HOST_USER,  # 发送邮箱，已经在settings.py设置，直接导入
        [info.resume.mail],  # 目标邮箱 切记此处只能是列表或元祖
        fail_silently=True,  # 发送失败是否返回错误信息
    )
    return

def search(request):
    types = Type.objects.all()
    jobs = Job.objects.all()
    if request.method == 'GET':
        return render(request, 'company/job.html', {'lists': jobs, 'types': types})
    if request.method == 'POST':
        kw = request.POST.get('kw')
        type = request.POST.get('type')
        row = request.POST.get('row')
        if type != 'all':
            print(0)
            jobs = jobs.filter(type_id=type)
        if kw:
            print(1)
            if row == 'workname':
                jobs = jobs.filter(name__icontains=kw)
            elif row == 'salary':
                print(int(kw))
                jobs = jobs.filter(salary_start__gte=int(kw))
        return render(request, 'company/job.html', {'lists': jobs, 'types': types, 'type': type})

def submit_number(request):
    types = Type.objects.all()
    jobs = Job.objects.order_by('heat').reverse()
    return render(request, 'company/job.html', {'lists': jobs, 'types': types, 'type': type})

def earliest_release(request):
    types = Type.objects.all()
    jobs = Job.objects.order_by('create')
    return render(request, 'company/job.html', {'lists': jobs, 'types': types, 'type': type})