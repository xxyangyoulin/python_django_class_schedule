# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=18, verbose_name=u"手机号", blank=True)

    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default='')
    avator = models.ImageField(upload_to='upload/avator/%Y%m', default='avator/default.png', max_length=100)

    introduce = models.TextField(default=u'', verbose_name=u"个人介绍")
    gender = models.IntegerField(choices=((0, u'男'), (1, u'女')), default=1)

    has_confirmed = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]

    def __unicode__(self):
        return self.username


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('UserProfile')
    type = models.IntegerField(u"验证码类型", choices=((0, u'邮箱'), (1, u'手机号')), default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

