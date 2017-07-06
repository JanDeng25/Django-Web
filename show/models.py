# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.

class Service(models.Model):
	name = models.CharField(max_length = 30)
	upload_date = models.DateTimeField('date upload')
	def __str__(self):
		return self.name

class File(models.Model):
	service = models.ForeignKey(Service, on_delete = models.CASCADE)
	#filename = models.CharField(max_length = 30)
	content = models.CharField(max_length = 200)
	upload_File = models.FileField(upload_to = './upload')
	upload_date = models.DateTimeField('date uploaded')
	def __str__(self):
		return self.content