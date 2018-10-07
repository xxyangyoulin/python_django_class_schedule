# coding=utf-8
import random
import string

import datetime

import hashlib
import json
from django.http import HttpResponse

from class_schedule import settings
from users.models import ConfirmString


def format_to_json(code, msg='', data=None):
    return json.dumps({'code': code, 'msg': msg, 'data': data})


def JsonResponse(code, msg='', data=None):
    return HttpResponse(format_to_json(code, msg=msg, data=data),
                        content_type='application/ajax')


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_32_id():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自MD课表的注册确认邮件。'

    text_content = '''感谢注册，请点击站点链接完成注册确认：{}?code={}
                    '''.format(settings.SITE_CONFIRM_URL, code)

    html_content = '''
                    <p>感谢注册，<a href="{host}?code={code}" target=blank>http://{host}/confirm/?code={code}</a>，\
                    <p>请点击站点链接完成注册确认！</p>
                    '''.format(host=settings.SITE_CONFIRM_URL, code=code)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
