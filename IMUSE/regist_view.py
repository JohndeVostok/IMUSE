#coding=utf-8

from django import forms
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from email_manager import send_email

class RegistForm(forms.Form): 
	username = forms.CharField(max_length = 50, widget = forms.TextInput(attrs = {"placeholder": "User ID"}))
	password_0 = forms.CharField(widget = forms.PasswordInput(attrs = {"placeholder": "Password"}))
	password_1 = forms.CharField(widget = forms.PasswordInput(attrs = {"placeholder": "Confirm Password"}))
	email = forms.EmailField(widget = forms.TextInput(attrs = {"placeholder": "Email Address"}))
	def clean(self):
		if (self.cleaned_data['password_0'] != self.cleaned_data['password_1']):
			raise forms.ValidationError("Passwords are not match")

		if (self.cleaned_data['username'] == self.cleaned_data['password_0']):
			raise forms.ValidationError("Password cannot be the same as user ID")

		if (len(self.cleaned_data['password_0']) < 6):
			raise forms.ValidationError("Password too short")

		if len(User.objects.filter(username = self.cleaned_data['username'])) > 0:
			raise forms.ValidationError("User ID existed")

		try:
			if len(User.objects.filter(email = self.cleaned_data['email'])) > 0:
				raise forms.ValidationError("Email already registered")
		except Exception as e:
			raise forms.ValidationError("Invalid Email Format")

		return self.cleaned_data

@csrf_protect
def regist(req):
	if req.method == 'POST':
		form = RegistForm(req.POST)
		if not form.is_valid():
			return render(req, 'regist.html' ,{'form': form})

		username = form.cleaned_data['username']
		password_0 = form.cleaned_data['password_0']
		password_1 = form.cleaned_data['password_1']
		email = form.cleaned_data['email']

		filter_result = User.objects.filter(username = username)

		user = User()
		user.username = username
		user.set_password(password_0)
		user.email = email
		user.save()
		new_user = auth.authenticate(username = username, password = password_0)
		if new_user is not None:
			auth.login(req, new_user)
			send_email(username + " Registration Complete", "User ID:" + username + "\nEmail:" + email + "\n")
			send_email("IMUSE Registration Complete", "User ID:" + username + "\nEmail:" + email + "\nWelcome to IMUSE.\n", email)
			return HttpResponseRedirect("/user/")
		else:
			raise Http404
	else:
		regist_form = RegistForm()
		return render(req, 'regist.html', {'form': regist_form})
