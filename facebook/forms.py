from django import forms
from .models import FacebookNewPage, FacebookNewPost
from .tasks import collect_page, collect_post

class FacebookPageForm(forms.ModelForm):
	class Meta:
		model = FacebookNewPage
		fields = ['url',]
		labels = {'url': 'ID/URL',}
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control col-md-9','placeholder':'Page_ID'}),
			'created_at': forms.SelectDateWidget(attrs={'class':'form-control'}),
		}
	def run_task(self):
		collect_page.delay(self.cleaned_data['url'])

class FacebookPostForm(forms.ModelForm):
	class Meta:
		model = FacebookNewPost
		fields = ['url',]
		labels = {'url': 'ID/URL',}
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control col-md-9','placeholder':'Post_ID'}),
			'created_at': forms.SelectDateWidget(attrs={'class':'form-control'}),
		}
	def run_task(self):
		collect_post.delay(self.cleaned_data['url'])
