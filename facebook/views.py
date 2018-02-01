from django.views.generic import CreateView, ListView, DeleteView, UpdateView, FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

from .models import FacebookNewPage, FacebookNewPost, Comment, Post
from .forms import FacebookPageForm, FacebookPostForm

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .tasks import collect_page, collect_post

class HomeView(TemplateView):
	template_name = "home.html"
	success_url = reverse_lazy('facebook:home')

class FacebookPageSearch(CreateView, ListView):
	model = FacebookNewPage
	form_class = FacebookPageForm
	template_name = 'new_page.html'
	success_url = reverse_lazy('facebook:new_page')
	def form_valid(self, form):
		self.object = form.save()
		form.run_task()
		return HttpResponseRedirect(self.get_success_url())

class FacebookPostSearch(CreateView, ListView):
	model = FacebookNewPost
	form_class = FacebookPostForm
	template_name = 'new_post.html'
	success_url = reverse_lazy('facebook:new_post')
	def form_valid(self, form):
		self.object = form.save()
		form.run_task()
		return HttpResponseRedirect(self.get_success_url())

class FacebookPostList(ListView):
	model = Post
	queryset = Post.objects.order_by('id')
	template_name = 'all_posts.html'
	paginate_by = 10

class FacebookCommentList(ListView):
	model = Comment
	queryset = Comment.objects.order_by('id')
	template_name = 'all_comments.html'
	paginate_by = 10

class FacebookPageUpdate(UpdateView):
	model = FacebookNewPage
	form_class = FacebookPageForm
	template_name = 'show_page.html'
	success_url = reverse_lazy('facebook:update_page')
	def get_context_data(self, **kwargs):
		context = super(FacebookPageUpdate, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.all()
		return context

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		if pk is not None:
			queryset = queryset.filter(pk=pk)
		obj = queryset.get()
		collect_page(obj.url)
		return obj

class FacebookPostUpdate(UpdateView):
	model = FacebookNewPost
	form_class = FacebookPostForm
	template_name = 'show_post.html'
	success_url = reverse_lazy('facebook:update_post')
	def get_context_data(self, **kwargs):
		context = super(FacebookPostUpdate, self).get_context_data(**kwargs)
		context['posts'] = Comment.objects.all()
		return context

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		if pk is not None:
			queryset = queryset.filter(pk=pk)
		obj = queryset.get()
		collect_post(obj.url)
		return obj

class FacebookPageDelete(DeleteView):
	model = FacebookNewPage
	template_name = 'delete_page.html'
	success_url = reverse_lazy('facebook:new_page')
	def get_context_data(self, **kwargs):
		context = super(FacebookPageDelete, self).get_context_data(**kwargs)
		context['posts']=Post.objects.filter(page=self.kwargs.get('pk'))
		return context

class FacebookPostDelete(DeleteView):
	model = FacebookNewPost
	template_name = 'delete_post.html'
	success_url = reverse_lazy('facebook:new_post')
	def get_context_data(self, **kwargs):
		context = super(FacebookPostDelete, self).get_context_data(**kwargs)
		context['comments']=Comment.objects.filter(page=self.kwargs.get('pk'))
		return context

class FacebookPageShow(DetailView):
	model = FacebookNewPage
	template_name = 'show_page.html'
	def get_context_data(self, **kwargs):
		context = super(FacebookPageShow, self).get_context_data(**kwargs)
		context['posts']=Post.objects.filter(page=self.kwargs.get('pk'))
		return context

class FacebookPostShow(DetailView):
	model = FacebookNewPost
	template_name = 'show_post.html'
	def get_context_data(self, **kwargs):
		context = super(FacebookPostShow, self).get_context_data(**kwargs)
		context['comments']=Comment.objects.filter(page=self.kwargs.get('pk'))
		return context
