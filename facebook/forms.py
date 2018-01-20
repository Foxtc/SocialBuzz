from django import forms
from .models import FacebookNewPage, FacebookNewPost

class FacebookPageForm(forms.ModelForm):
	class Meta:
		model = FacebookNewPage
		fields = ['url',]
		labels = {'url': 'ID/URL',}
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control col-md-9','placeholder':'ID/URL'}),
			'created_at': forms.SelectDateWidget(attrs={'class':'form-control'}),
		}

class FacebookPostForm(forms.ModelForm):
	class Meta:
		model = FacebookNewPost
		fields = ['url',]
		labels = {'url': 'ID/URL',}
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control col-md-9','placeholder':'ID/URL'}),
			'created_at': forms.SelectDateWidget(attrs={'class':'form-control'}),
		}
