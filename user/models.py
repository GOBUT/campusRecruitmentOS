from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
    '''用户模型类'''

    # 扩展系统自带的User
    photo = models.ImageField(upload_to='user', verbose_name='照片', default='', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='审核通过')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Resume(models.Model):
    id = models.AutoField(primary_key=True)  # 自增长类型
    user = models.ForeignKey('User', verbose_name='用户', on_delete=models.CASCADE)
    name = models.CharField(max_length=40, verbose_name='姓名', default='', blank=True, null=True)
    sex = models.CharField(max_length=5, verbose_name='性别', default='', blank=True, null=True)
    birth = models.DateField(verbose_name='出生年月', blank=True, null=True)
    registration = models.CharField(max_length=50, verbose_name='户籍所在地', default='', blank=True, null=True)
    now = models.CharField(max_length=50, verbose_name='居住城市', default='', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='电话', default='', blank=True, null=True)
    mail = models.CharField(max_length=20, verbose_name='邮箱', default='', blank=True, null=True)
    photo = models.ImageField(upload_to='static/images/user', verbose_name='照片', default='', blank=True, null=True)
    job = models.CharField(max_length=20, verbose_name='求职岗位', default='', blank=True, null=True)
    salary = models.CharField(max_length=20, verbose_name='薪资要求', default='', blank=True, null=True)
    education = models.CharField(max_length=1000, verbose_name='教育经历', default='', blank=True, null=True)
    subject = models.CharField(max_length=1000, verbose_name='项目经历', default='', blank=True, null=True)
    language = models.CharField(max_length=300, verbose_name='语言能力', default='', blank=True, null=True)
    skill = models.CharField(max_length=300, verbose_name='专业技能', default='', blank=True, null=True)
    certificates = models.CharField(max_length=300, verbose_name='证书', default='', blank=True, null=True)
    evaluation = models.CharField(max_length=300, verbose_name='自我评价', default='', blank=True, null=True)

    class Meta:
        db_table = 'resume'
        verbose_name = '简历管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SearchData(models.Model):
    svalue =  models.CharField(max_length=300,verbose_name='字段', default='', blank=True, null=True)
    snumble = models.IntegerField(verbose_name='出现次数',default=0)

    class Meta:
        db_table = 'searchdata'
        verbose_name = '词云管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name