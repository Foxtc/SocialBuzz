from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

from .models import FacebookPage
from .forms import FacebookPageForm
#from .filters import FacebookPageFilter

from fb_data_collector import FacebookAuthenticator
from fb_data_collector import FacebookPostsCollector
from fb_data_collector import FacebookCommentsCollector
import json, codecs

from django.shortcuts import render

# Create your views here.

class FacebookPageCreate(CreateView):
	model = FacebookPage
	form_class = FacebookPageForm
	template_name = 'pages/page_form.html'
	success_url = reverse_lazy('facebook:list_page')


class FacebookPageList(ListView):
	queryset = FacebookPage.objects.order_by('page_id')
	template_name = 'pages/page_list.html'
	paginate_by = 5

class FacebookPageUpdate(UpdateView):
	model = FacebookPage
	form_class = FacebookPageForm
	template_name = 'pages/page_form.html'
	success_url = reverse_lazy('facebook:list_page')

class FacebookPageDelete(DeleteView):
	model = FacebookPage
	template_name = 'pages/page_delete.html'
	success_url = reverse_lazy('facebook:list_page')

class FacebookPageShow(DetailView):
	model = FacebookPage
	template_name = 'pages/page_show.html'

    #below, client_id and client_secret should be your actual client ID and secret
	app_id = "1113647168736591"
	client_secret = "567c460931e1bbb017932b9361fd877a"

	fb_auth = FacebookAuthenticator(app_id,client_secret)
	fb_access_token = fb_auth.request_access_token()

	#to get page posts
	posts_collector = FacebookPostsCollector(fb_access_token)
	posts = posts_collector.collect("barackobama",max_rows=100)

	#to get comments on a single post
	comments_collector = FacebookCommentsCollector(fb_access_token)
	post_id = "6815841748_10155375836346749"

	comments = comments_collector.collect(post_id,max_rows=100)
	results = json.dumps(posts)
	render("pages/pages_show.html", {'results':results})
