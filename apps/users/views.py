# coding=utf-8

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from users.forms import LoginForm
from users.models import UserProfile, ConfirmString
from users.utils import JsonResponse, make_confirm_string, send_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print e.message
            return None


# class LoginView(View):
#     def get(self, request):
#         print 'get'
#
#     def post(self, request):
#         print "post"

# @csrf_exempt
# def dispatch(self, *args, **kwargs):
#   return super(MyView, self).dispatch(*args, **kwargs)


class RegisterView(View):
    def get(self, request):
        print 'get'

    @csrf_exempt
    def post(self, request):
        print RegisterView.__name__ + " post"

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            if "@" in username:  # as email
                same_name_user = UserProfile.objects.filter(Q(email=username))
                if same_name_user:
                    print same_name_user
                    return JsonResponse(2, u"邮箱已经被注册")

                new_user = UserProfile.objects.create_user(username, username, password)
                code = make_confirm_string(new_user)
                try:
                    send_email(username, code)
                    return JsonResponse(1, u'使用邮箱注册成功，请及时去邮箱验证！')
                except:
                    return JsonResponse(2, u'邮箱验证发送失败！')

            else:
                try:
                    mobile = int(username)  # as number

                    same_name_user = UserProfile.objects.filter(Q(mobile=username))
                    if same_name_user:
                        print same_name_user
                        return JsonResponse(2, u"手机号已经被注册")
                    return JsonResponse(2, u'未开放手机注册')
                except:
                    return JsonResponse(2, u'非邮箱或手机号')
        else:
            return JsonResponse(3, "数据验证错误", login_form.errors)


class LoginView(View):
    def get(self, request):
        return render(request, 'login/login.html', locals())

    @csrf_exempt
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            login_user = authenticate(username=username, password=password)

            if login_user is not None:
                login(request, login_user)
                return JsonResponse(1, u"登录成功")
            else:
                massage = u"邮箱或密码错误"
                return JsonResponse(2, massage, login_form.errors)
        else:
            return JsonResponse(3, "数据验证错误", login_form.errors)


class LogoutView(View):
    def get(self, request):
        logout(request)
        massage = u'注销成功'
        return JsonResponse(1, massage)


def info(request):
    # data = dict()
    # data['email'] = "sdf"
    # data['username'] = "fff"
    # return JsonResponse(1, u"成功", data)

    if request.user.is_authenticated():
        data = dict()
        data['email'] = request.user.email
        return JsonResponse(1, u"成功", data)
    else:
        return JsonResponse(3, u'未登录')


def user_confirm(request):
    """
    用户验证
    """
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求，或已确认完毕!'
        return render(request, 'login/confirm.html', locals())

    confirm.user.has_confirmed = True
    confirm.user.save()
    confirm.delete()
    message = '确认成功，谢谢！'
    return render(request, 'login/confirm.html', locals())


class PasswordView(View):
    def get(self, request):
        return render(request, 'login/password.html')

    def post(self, request):
        pass
