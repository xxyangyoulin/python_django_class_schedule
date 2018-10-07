"""class_schedule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from main.views import IndexView, UploadCourseView, DownCourseView, ShareView, check_update

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name="index"),
    url(r'^upload_course/$', csrf_exempt(UploadCourseView.as_view()), name="upload_course"),
    url(r'^down_course/$', csrf_exempt(DownCourseView.as_view()), name="down_course"),
    url(r'^share/$', csrf_exempt(ShareView.as_view()), name="upload_share"),
    url(r'^check_update/$', check_update, name="check_update"),
]
