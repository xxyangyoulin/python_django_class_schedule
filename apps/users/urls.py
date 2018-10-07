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

from users import views
from users.views import LoginView, RegisterView, LogoutView, PasswordView

urlpatterns = [
    url(r'^login/$', csrf_exempt(LoginView.as_view()), name='login'),
    url(r'^register/$', csrf_exempt(RegisterView.as_view()), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^confirm/$', views.user_confirm, name="confirm"),
    url(r'^info/$', views.info, name="info"),
    url(r'^password/$', PasswordView.as_view(), name="password"),
]
