from django.views.generic import CreateView, ListView, DeleteView, UpdateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

from .models import FacebookNewPage, FacebookNewPost, Comment, Post
from .forms import FacebookPageForm, FacebookPostForm, HomeForm

from django.shortcuts import render

class Home():
	form_class = HomeForm
	success_url = reverse_lazy('facebook:home')

class FacebookPageSearch(CreateView, ListView):
	model = FacebookNewPage
	form_class = FacebookPageForm
	template_name = 'home.html'
	success_url = reverse_lazy('facebook:new_page')
	context_object_name = 'page_new'

class FacebookPostSearch(CreateView, ListView):
	model = FacebookNewPost
	form_class = FacebookPostForm
	template_name = 'home.html'
	success_url = reverse_lazy('facebook:new_post')
	context_object_name = 'post_list'

class FacebookPostList(ListView):
	model = Post
	queryset = Post.objects.order_by('id')
	template_name = 'post_list.html'
	paginate_by = 10

class FacebookCommentList(ListView):
	model = Comment
	queryset = Comment.objects.order_by('id')
	template_name = 'comment_list.html'
	paginate_by = 10

class FacebookPageUpdate(UpdateView):
	model = FacebookNewPage
	form_class = FacebookPageForm
	template_name = 'home.html'
	success_url = reverse_lazy('facebook:list_post')

class FacebookPageDelete(DeleteView):
	model = FacebookNewPage
	template_name = 'delete.html'
	success_url = reverse_lazy('facebook:new_search')

class FacebookPageShow(DetailView):
	model = FacebookNewPage
	template_name = 'show.html'
