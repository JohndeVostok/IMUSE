#coding=utf-8
from django import forms
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from regist_view import regist
from login_view import login
from apply_view import fill_apply_form
#from models import User

@login_required(login_url = '/login/')
def index(req):
#	raise Http404
	username = req.user
	return render(req, 'index.html', {'username': username})

def logout(req):
	auth.logout(req)
	return HttpResponseRedirect("/login/")

def success(req):
	return render(req, 'success.html')

def page_not_found(req):
	return render(req, '404.html')
