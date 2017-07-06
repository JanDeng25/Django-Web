#from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
	context = {}
	context['string'] = "Welcome to GFF!"
	return render(request, 'index.html', context)
#	return HttpResponse("Welcome to GFF!")
