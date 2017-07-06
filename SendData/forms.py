from django import forms

class senddata(forms.Form):
	ip_addr = forms.CharField(max_length = 15)
	port = forms.CharField(max_length = 5)
	data = forms.CharField(max_length = 50)