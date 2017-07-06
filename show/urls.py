"""GFF URL Configuration

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
from django.conf.urls import *
import show.views

urlpatterns = [

    url(r'^$', show.views.upload, name = 'show'),
    #url(r'upload/', show.views.upload, name = 'upload'),
    url(r'upload_file/(.+)/', show.views.upload_file, name = 'upload_file'),
    url(r'download_file/(.+)/', show.views.download_file, name = 'download_file'),
    url(r'modify_file/(?P<id>[^ ]*) (?P<fn>[^ ]*) (?P<cont>.*)/', show.views.modify_file, name = 'modify_file'),

    url(r'file_detail/(.+)/', show.views.file_detail, name = 'file_detail'),

    url(r'service_list/', show.views.service_list, name = 'service_list'),
    url(r'service_today/', show.views.service_today, name = 'service_today'),
    url(r'service_today_page/', show.views.service_today_page, name = 'service_today_page'),
    #url(r'^admin/', admin.site.urls),
]

