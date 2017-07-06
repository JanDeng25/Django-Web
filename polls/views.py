# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from polls.models import *
from django.utils import timezone

class FileForm(forms.Form):
	servicename = forms.CharField()
	content = forms.CharField()
	upload_File = forms.FileField()

def upload(request):
	if request.method == "POST":
		ff = FileForm(request.POST, request.FILES)
		if ff.is_valid():
			#获取表单信息
			servicename = ff.cleaned_data['servicename']
			content = ff.cleaned_data['content']
			upload_File = ff.cleaned_data['upload_File']
			#写入数据库
			s = Service()
			s.servicename = servicename
			s.service_uploaddate = timezone.now()
			s.save()
			f = File()
			f.service = s
			f.content = content
			f.upload_File = upload_File
			f.uploaddate = timezone.now()
			f.save()
			
			services = Service.objects.order_by('servicename')   #distinct表示重复出现只选取一次
			return render_to_response('service_list.html',{'services':services})
			#return HttpResponse('upload successfully!')
	else:
		ff = FileForm()
	return render(request, 'upload.html',{'ff':ff})

def service_list(request):
	services = Serv.objects.order_by('servicename')     #distinct表示重复出现只选取一次
	return render_to_response('service_list.html',{'services':services})

#def file_detail(request):
#	files = File.objects.order_by('-uploaddate').all()     #负号表示降序
#	return render_to_response('file_detail.html',{'files':files})

def file_detail(request, fn):
	files = File.objects.order_by('-uploaddate')
	return render_to_response('file_detail.html', {'files':files})


# Create your views here.
