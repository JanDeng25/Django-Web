# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from socket import *
from time import *
def send(request):
	return render(request, 'send.html')

def senddata(request):
	
	HOST = request.POST.get('ip')
	if not HOST:
		return render(request, 'send.html')
	PORT = request.POST.get('port', 1)
	BUFSIZE = 1024
	ADDR = (HOST, int(PORT))
	timeout = 20
	#setdefaulttimeout(timeout)
	udpSocket = socket(AF_INET, SOCK_DGRAM)

	data = request.POST.get('data')
	#if not data:
		#break;
	udpSocket.sendto(data, ADDR)
		#sleep(timeout)
	data, ADDR = udpSocket.recvfrom(BUFSIZE)
	#if not data:
		#break;
	print data
	udpSocket.close()
	return render(request, 'success.html')


# Create your views here.
