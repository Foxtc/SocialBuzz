from django.views.generic import CreateView, ListView, DeleteView, UpdateView, FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

from .models import FacebookNewPage, FacebookNewPost, Comment, Post
from .forms import FacebookPageForm, FacebookPostForm

from django.shortcuts import render
from .tasks import collect_search
from django.http import HttpResponseRedirect

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
		#collect_search(form.widgets['url'])
		form.run_task()
		return HttpResponseRedirect(self.get_success_url())

class FacebookPostSearch(CreateView, ListView):
	model = FacebookNewPost
	form_class = FacebookPostForm
	template_name = 'new_post.html'
	success_url = reverse_lazy('facebook:new_post')
	def form_valid(self, form):
		self.object = form.save()
		#collect_search(form.widgets['url'])
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
	template_name = 'home.html'
	success_url = reverse_lazy('facebook:list_post')

class FacebookPageDelete(DeleteView):
	model = FacebookNewPage
	template_name = 'delete.html'
	success_url = reverse_lazy('facebook:new_search')

class FacebookPageShow(DetailView):
	model = FacebookNewPage
	template_name = 'show_page.html'

class FacebookPostShow(DetailView):
	model = FacebookNewPost
	template_name = 'show_post.html'
