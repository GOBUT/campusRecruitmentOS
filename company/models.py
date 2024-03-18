from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.AutoField(primary_key=True)  # 自增长类型
    username = models.CharField(max_length=20, verbose_name='账户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    name = models.CharField(max_length=40, verbose_name='公司名称')
    phone = models.CharField(max_length=20, verbose_name='电话')
    mail = models.CharField(max_length=20, verbose_name='邮箱')
    photo = models.ImageField(upload_to='static/images/company', verbose_name='照片')
    address = models.CharField(max_length=300, verbose_name='公司地址')
    info = models.CharField(max_length=1000, verbose_name='公司介绍')
    status=models.BooleanField(default=False, verbose_name='审核通过')

    class Meta:
        db_table = 'company'
        verbose_name = '企业管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Type(models.Model):
    id = models.AutoField(primary_key=True)  # 自增长类型
    name = models.CharField(max_length=100, verbose_name='职位类型')

    class Meta:
        db_table = 'type'
        verbose_name = '职位类型管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Job(models.Model):
    id = models.AutoField(primary_key=True)  # 自增长类型
    name = models.CharField(max_length=100, verbose_name='职位名称')
    workcity = models.CharField(max_length=50, verbose_name='工作城市')
    company = models.ForeignKey('Company', verbose_name='企业', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', verbose_name='职位类型', on_delete=models.CASCADE)
    salary_start  = models.IntegerField(verbose_name='最低薪资')
    salary_end = models.IntegerField(verbose_name='最高薪资')
    salary = models.CharField(max_length=200, verbose_name='薪资要求')
    education  = models.CharField(max_length=200, verbose_name='学历要求')
    experience  = models.CharField(max_length=200, verbose_name='经验要求')
    content = models.CharField(max_length=600, verbose_name='职位需求')
    create = models.DateTimeField(auto_now_add=True, max_length=200, verbose_name='发布日期')
    heat = models.IntegerField(default=0,verbose_name='热度')
    pv = models.IntegerField(default=0, verbose_name='浏览量')

    class Meta:
        db_table = 'job'
        verbose_name = '职位管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Send(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='订单id')  # 自增长类型
    resume = models.ForeignKey('user.Resume', verbose_name='简历', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', verbose_name='职位', on_delete=models.CASCADE)
    uid = models.ForeignKey('user.User', verbose_name='用户ID', on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True, max_length=200, verbose_name='投递时间')
    status_choice = (
        (1, '投递成功'),
        (2, '被查看'),
        (3, '邀面试'),
        (4, '不合适')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=1)

    class Meta:
        db_table = 'send'
        verbose_name = '简历投递管理'
        verbose_name_plural = verbose_name


class Interview(models.Model):
    id = models.AutoField(primary_key=True)  # 自增长类型
    user = models.ForeignKey('user.User', verbose_name='应聘者', on_delete=models.CASCADE)
    resume = models.ForeignKey('user.Resume', verbose_name='简历', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', verbose_name='企业', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', verbose_name='职位', on_delete=models.CASCADE)
    user_choice = (
        (1, '待处理'),
        (2, '已接受'),
        (3, '已拒绝')
    )
    user_status = models.SmallIntegerField(verbose_name='应聘者状态', choices=user_choice, default=1)
    status_choice = (
        (1, '未开始'),
        (2, '未通过'),
        (3, '已通过')
    )
    status = models.SmallIntegerField(verbose_name='面试结果', choices=status_choice, default=1)
    time = models.DateTimeField(max_length=200, verbose_name='面试时间', null=True, blank=True, default=None)
    meetingid = models.CharField(max_length=100, verbose_name='会议号',default='')
    create = models.DateTimeField(auto_now_add=True, max_length=200, verbose_name='发布时间')

    class Meta:
        db_table = 'interview'
        verbose_name = '面试邀请管理'
        verbose_name_plural = verbose_name
