from django import forms
from .models import FacebookNewPage, FacebookNewPost
from .tasks import collect_search

class FacebookPageForm(forms.ModelForm):
	class Meta:
		model = FacebookNewPage
		fields = ['url',]
		labels = {'url': 'ID/URL',}
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control col-md-9','placeholder':'Page_ID/URL'}),
			'created_at': forms.SelectDateWidget(attrs={'class':'form-control'}),
		}
	def run_task(self):
		collect_search.delay(self.cleaned_data['url'])

class FacebookPostForm(forms.ModelForm):
	class Meta:
		model = FacebookNewPost
		fields = ['url',]
		labels = {'url': 'ID/URL',}
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control col-md-9','placeholder':'Post_ID/URL'}),
			'created_at': forms.SelectDateWidget(attrs={'class':'form-control'}),
		}
