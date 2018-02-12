#coding=utf-8
from django import forms
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from regist_view import regist
#from models import User

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 50, widget = forms.TextInput(attrs = {"placeholder": "User ID"}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {"placeholder": "Password"}))

	def clean(self):
		if (auth.authenticate(username = self.cleaned_data['username'], password = self.cleaned_data['password'])) is None:
			raise forms.ValidationError("Invalid handle or password")
		return self.cleaned_data

@csrf_protect
def login(req):
	if req.method == 'POST':
		form = LoginForm(req.POST)
		if not form.is_valid():
			return render(req, 'login.html', {'form': form})

		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(req, user)
			return HttpResponseRedirect("/user/")
		else:
			raise Http404
	else:
		login_form = LoginForm()
		return render(req, 'login.html', {'form': login_form})

