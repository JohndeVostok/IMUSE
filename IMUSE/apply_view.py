import re
from django import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from email_manager import send_email

class ApplyForm(forms.Form):
	name = forms.CharField(max_length = 50)
	pinyin = forms.CharField(max_length = 50)
	gender = forms.CharField(widget = forms.Select(choices = (("Male", "Male"), ("Female", "Female"), ("Trans", "Trans"))))
	place = forms.DateField(widget = forms.SelectDateWidget(empty_label = ("Choose Year", "Choose Month", "Choose Day"), years=reversed(range(1980, 2018))))
	group = forms.CharField(max_length = 50)
	mobile = forms.CharField(max_length = 50)
	nation = forms.CharField(max_length = 50)
	wechat = forms.CharField(max_length = 50)

	university = forms.CharField(max_length = 50)
	study_year = forms.CharField(widget = forms.Select(choices = tuple([(str(i), str(i)) for i in range(1, 16)])))
	study_field = forms.CharField(max_length = 50)

	education = forms.CharField(widget = forms.Textarea())
	employment = forms.CharField(widget = forms.Textarea())
	association = forms.CharField(widget = forms.Textarea())
	performance = forms.CharField(widget = forms.Textarea())
	essay = forms.CharField(widget = forms.Textarea())
	cv = forms.CharField(widget = forms.Textarea())
	scholarship = forms.CharField(widget = forms.Textarea())
	signature = forms.CharField(max_length = 50)
	date = 	birth_date = forms.DateField(widget = forms.SelectDateWidget(empty_label = ("Choose Year", "Choose Month", "Choose Day"), years = range(2017, 2030)))

	def clean(self):
		if len(re.sub(r'([0-9]|\+|\-)', '', self.cleaned_data["mobile"])) > 0:
			raise forms.ValidationError('Invalid mobile phone number.')
		return self.cleaned_data

@csrf_protect
@login_required(login_url = '/login/')
def fill_apply_form(req):
	if req.method == 'POST':
		form = ApplyForm(req.POST)
		if not form.is_valid():
			return render(req, 'apply.html', {'form': form})
		else:
			user = req.user
			email_title = user.username + " Application Complete"
			email_context = "User ID: " + user.username + "\n"
			email_context += "Email: " + user.email + "\n"
			for (i, j) in form.cleaned_data.items():
				if (i == 'birth_date' or i == 'date'):
					email_context += i + ": " + j.strftime("%Y-%m-%d\n")
					
				else:
					email_context += i + ": " + j + "\n"

			send_email(email_title, email_context)
			send_email("IMUSE Application Complete", "Welcome to IMUSE.\nPlease wait for our verification.\nThank you for your patience.\n", user.email)

			return HttpResponseRedirect("/success/");
	else:
		apply_form = ApplyForm()
		return render(req, "apply.html", {'form': apply_form})
