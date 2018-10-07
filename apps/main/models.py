# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class AppVersion(models.Model):
    version_code = models.IntegerField(verbose_name=u'版本号', null=False, blank=False)
    version_name = models.CharField(verbose_name=u'版本名称', default="", max_length=16)
    describe = models.CharField(verbose_name=u'描述', default='无说明', max_length=256)
    release = models.BooleanField(verbose_name=u'是否发布', default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'APP版本'
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]

    def __unicode__(self):
        return self.version_name


class CourseGroup(models.Model):
    name = models.CharField(null=False, blank=False, max_length=128, verbose_name=u"名称")
    school_class = models.CharField(default=u"", max_length=128, verbose_name=u'课表所属')
    share = models.BooleanField(default=False, verbose_name=u'是否分享')
    share_id = models.CharField(verbose_name=u'分享id', max_length=32, null=True)

    user = models.ForeignKey(to=u'users.UserProfile', to_field='id', verbose_name=u"所属用户", null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '课程组'
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]

    def __unicode__(self):
        return self.name


class CourseItem(models.Model):
    name = models.CharField(null=False, blank=False, max_length=128, verbose_name=u"名称")
    teacher = models.CharField(default=u'', max_length=32, verbose_name=u"老师")
    location = models.CharField(default=u"", max_length=128, verbose_name=u"上课地点")
    color = models.IntegerField(default=0x88888888, verbose_name=u'颜色')

    time_which_day = models.IntegerField(null=False, blank=False, verbose_name=u"周几")
    time_all_week = models.CharField(default='-', max_length=512, verbose_name=u'周 空代表所有')
    start_node = models.IntegerField(verbose_name=u"开始节数")
    node_count = models.IntegerField(verbose_name=u"总节数")
    only_id = models.CharField(verbose_name='唯一标识', default=u'', max_length=32)
    group = models.ForeignKey(to="CourseGroup", to_field="id", verbose_name=u'所属组')
    create_time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(verbose_name=u'是否删除', default=False)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]

    def __unicode__(self):
        return self.name
