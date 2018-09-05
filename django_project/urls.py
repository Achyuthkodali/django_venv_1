"""django_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login_auth', check_login),
    url(r'^register_auth', check_register),
    url(r'^edit_profile', edit_profile),
    url(r'^jaja', jaja),
    url(r'^change_password', change_password),
    url(r'^upload_avatar', upload_avatar),
    url(r'^mail_test', mail_test),
    url(r'^activate_user', activate_user)
]
