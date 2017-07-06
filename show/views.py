# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from show.models import *
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse	

# Create your views here.
class FileForm(forms.Form):
	service_name = forms.CharField(label = '服务')
	content = forms.CharField(label = '文件描述')
	upload_File = forms.FileField(label = '上传文件')

class ConfigForm(ModelForm):
	content = forms.CharField(label = '文件描述')
	upload_File = forms.FileField(label = '上传文件', required = False)
	class Meta:
		model = File
		fields = ('content', 'upload_File')

def upload(request):
	if request.method == "POST":
		ff = FileForm(request.POST, request.FILES)
		if ff.is_valid():
			name = ff.cleaned_data['service_name']
			content = ff.cleaned_data['content']
			upload_File = ff.cleaned_data['upload_File']

			s = Service.objects.filter(name = name) #get和filter有区别
			if s.count() == 0:
				s = Service()
				s.name = name
				s.upload_date =timezone.now()
				s.save()	
			else:
				s = Service.objects.get(name = name)
				s.upload_date =timezone.now()
				s.save()
			f = File()
			f.service = s
			f.content = content
			f.upload_File = upload_File
			f.upload_date = timezone.now()
			f.save()
			services = Service.objects.order_by('name')
			return render_to_response('service_list.html',{'services':services})
	else:
		ff = FileForm()
	return render(request, 'upload.html', {'ff':ff})

#上传配置文件
def upload_file(request, fn):
	if request.method == "POST":
		ff = ConfigForm(request.POST, request.FILES)
		if ff.is_valid():
			#name = ff.cleaned_data['service_name']
			content = ff.cleaned_data['content']
			upload_File = ff.cleaned_data['upload_File']
			s = Service.objects.get(name = fn)
			s.upload_date =timezone.now()
			s.save()
			f = File()
			f.service = s
			f.content = content
			f.upload_File = upload_File
			f.upload_date = timezone.now()
			f.save()
			services = Service.objects.get(name = fn)
			files = services.file_set.order_by('-upload_date')
			return HttpResponseRedirect(reverse('show:file_detail', args = [fn]))
	else:
		ff = ConfigForm()
	return render(request, 'upload.html', locals())


#修改配置文件：读取原文件有bug
def modify_file(request, id, fn, cont):
	if request.method == "POST":
		ff = ConfigForm(request.POST, request.FILES)
		if ff.is_valid():
			#name = ff.cleaned_data['service_name']
			content = ff.cleaned_data['content']
			upload_File = ff.cleaned_data['upload_File']
			s = Service.objects.get(name = fn)
			s.upload_date =timezone.now()
			s.save()
			f = s.file_set.get(id = id)
			f.content = content
			if upload_File:
				f.upload_File = upload_File
			f.upload_date = timezone.now()
			f.save()
			services = Service.objects.get(name = fn)
			files = services.file_set.order_by('-upload_date')

			#return render_to_response('file_detail.html',locals())
			return HttpResponseRedirect(reverse('show:file_detail', args = [fn]))
	else:
		s = Service.objects.get(name = fn)
		f = s.file_set.get(id = id)
		ff = ConfigForm(instance = f)
	return render(request, 'upload.html', locals())

#服务列表(分页)
def service_list(request):
	services = Service.objects.all()   #distinct表示重复出现只选取一次
	current_page = request.GET.get('p')
	keyword = request.GET.get("search","")
	if keyword:
		services = services.filter(name__contains = keyword)
	#每页显示10条记录
	paginator = Paginator(services, 1)
	try:
		posts = paginator.page(current_page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'service_list.html', locals())

#服务的配置列表
def file_detail(request,fn):
	s = Service.objects.get(name = fn)
	files = s.file_set.order_by('-upload_date')
	current_page = request.GET.get('p')
	keyword = request.GET.get("search","")
	if keyword:
		files = files.filter(content__contains = keyword)
	#每页显示10条记录
	paginator = Paginator(files, 5)
	try:
		posts = paginator.page(current_page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'file_detail.html', locals())

#下载文件
def download_file(request, fn):
	#从第七个字母读取文件名
	the_file_name = fn[7:]
	filename = fn
	response = StreamingHttpResponse(readFile(filename))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name);
	return response

def readFile(filename, chunk_size = 512):
	with open(filename, 'rb') as f:
		while True:
			c = f.read(chunk_size)
			if c:
				yield c
			else:
				break

#from django.views.decorators.csrf import csrf_protect
#@csrf_protect
def service_today(request):
	current_page = request.GET.get('p')
	services = Service.objects.filter(upload_date__startswith = timezone.now().date())
	keyword = request.GET.get("search","")
	if keyword:
		services = services.filter(name__contains = keyword)
	#每页显示1条记录
	paginator = Paginator(services, 1)
	try:
		posts = paginator.page(current_page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'service_today.html', locals())

def service_oneday(request, y, m, d):
	services = Service.objects.filter(upload_date__year = y, upload_date_month = m, upload_date_day = d)
	return render_to_response('service_today.html', locals())

#分页显示今天更新的服务列表
def service_today_page(request):
	current_page = request.GET.get('p')
	services = Service.objects.filter(upload_date__startswith = timezone.now().date())
	#每页显示1条记录
	paginator = Paginator(services, 1)
	try:
		posts = paginator.page(current_page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except:
		posts = paginator.page(paginator.num_pages)

	return render_to_response('service_today_page.html', locals())
"""
def search_service(request):
	servies = Service.objects.all()
	keyword = request.POST['search_words']
	#services = Service.objects.filter(name__contains = keyword | upload_date__contains = keyword)  #contain关键字
	
	return HttpResponse("search services")

def file_search(request, fn):
	keyword = request.POST['search_words']
	s = Service.objects.get(name = fn)
	files = s.file_set.filter(content__contains = keyword | upload_date__contains = keyword)
	return HttpResponse("search files")
"""