# coding=utf-8
import json

# Create your views here.
from django.shortcuts import render
from django.views.generic import View

from main.models import CourseGroup, CourseItem, AppVersion
from users.utils import JsonResponse, make_32_id


# only_id在分享的和未分享的可能会重复，where需要加入用户进行再判断

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class UploadCourseView(View):
    def post(self, request):
        if request.user.is_authenticated():
            try:
                data_dict = json.loads(request.body.decode("utf-8"))
                print data_dict
                data_list = data_dict['data']
            except:
                return JsonResponse(3, u"上传的数据有误")
            user = request.user
            for item in data_list:
                group_name = item['group_name']
                course_group, created = CourseGroup.objects \
                    .get_or_create(user=user, name=group_name, share=False)

                try:
                    old_course = CourseItem.objects \
                        .filter(only_id=item['only_id'], group=course_group) \
                        .get()
                    if item['deleted']:
                        old_course.delete()
                        continue
                except:
                    if item['deleted']:
                        continue
                    old_course = CourseItem()

                old_course.group = course_group
                old_course.only_id = item['only_id']
                old_course.name = item['name']
                old_course.teacher = item['teacher']
                old_course.location = item['location']
                old_course.color = item['color']
                old_course.time_all_week = item['all_week']
                old_course.start_node = item['start_node']
                old_course.node_count = item['node_count']
                old_course.time_which_day = item['week']
                old_course.deleted = item['deleted']
                old_course.only_id = item['only_id']

                old_course.save()  # 该方法在存在id的情况是更新
            return JsonResponse(1, u"成功")
        return JsonResponse(3, u"未登录")


class DownCourseView(View):
    def post(self, request):
        if request.user.is_authenticated():
            user = request.user
            course_group = CourseGroup.objects.filter(user=user).all()
            if course_group:
                item_list = list()
                has_data = False
                for group in course_group:
                    items = CourseItem.objects.filter(group=group, deleted=False)
                    if items:
                        has_data = True
                        for item in items:
                            item_dict = dict()
                            item_dict['name'] = item.name
                            item_dict['teacher'] = item.teacher
                            item_dict['location'] = item.location
                            item_dict['week'] = item.time_which_day
                            item_dict['all_week'] = item.time_all_week
                            item_dict['start_node'] = item.start_node
                            item_dict['node_count'] = item.node_count
                            item_dict['color'] = item.color
                            item_dict['group_name'] = group.name
                            item_dict['only_id'] = item.only_id

                            item_list.append(item_dict)
                if not has_data:
                    return JsonResponse(2, u'未找到任何数据')
                return JsonResponse(1, u"成功", item_list)
            else:
                return JsonResponse(2, u'未找到任何数据')
        else:
            return JsonResponse(3, u"未登录")


class ShareView(View):
    def post(self, request):
        try:
            data_dict = json.loads(request.body.decode("utf-8"))
            print  data_dict
            data_list = data_dict['data']
        except:
            return JsonResponse(3, u"上传的数据有误")
        if len(data_list) == 0:
            return JsonResponse(3, u"上传的数据为空")

        share_group = CourseGroup()
        share_group.name = data_list[0]['group_name']
        share_group.share = True
        share_group.share_id = make_32_id()
        try:
            share_group.user = request.user
        except:
            pass
        share_group.save()
        for item in data_list:
            course = CourseItem()
            course.name = item['name']
            course.teacher = item['teacher']
            course.location = item['location']
            course.color = item['color']
            course.time_all_week = item['all_week']
            course.start_node = item['start_node']
            course.node_count = item['node_count']
            course.time_which_day = item['week']
            course.deleted = False
            course.group = share_group
            course.save()
        return JsonResponse(1, u"分享成功", data=share_group.share_id)

    def get(self, request):
        try:
            share_id = request.GET.get('id')
            share_group = CourseGroup.objects.filter(share_id=share_id, share=True).get()
            courses = CourseItem.objects.filter(group=share_group).all()
            result_list = list()
            for item in courses:
                item_dict = dict()
                item_dict['name'] = item.name
                item_dict['teacher'] = item.teacher
                item_dict['location'] = item.location
                item_dict['week'] = item.time_which_day
                item_dict['all_week'] = item.time_all_week
                item_dict['start_node'] = item.start_node
                item_dict['node_count'] = item.node_count
                item_dict['color'] = item.color
                item_dict['group_name'] = share_group.name
                result_list.append(item_dict)
            return JsonResponse(1, u"成功", result_list)
        except:
            return JsonResponse(3, u"该分享已经不在地球上了")


def check_update(request):
    version = AppVersion.objects.filter(release=True).order_by('-version_code').first()

    return JsonResponse(1, u"成功", data={'code': version.version_code,
                                        'name': version.version_name,
                                        'describe': version.describe})
