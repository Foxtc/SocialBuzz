from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

from .models import FacebookPage
from .forms import FacebookPageForm
from .models import Post

# Create your views here.

class FacebookPageCreate(CreateView, ListView):
	model = FacebookPage
	form_class = FacebookPageForm
	template_name = 'page_form.html'
	success_url = reverse_lazy('facebook:new_page')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pages'] = FacebookPage.objects.all()
		return context

class FacebookPageList(ListView):
	model = Post
	queryset = Post.objects.order_by('id')
	template_name = 'page_list.html'
	paginate_by = 10

class FacebookPageUpdate(UpdateView):
	model = FacebookPage
	form_class = FacebookPageForm
	template_name = 'page_form.html'
	success_url = reverse_lazy('facebook:list_page')

class FacebookPageDelete(DeleteView):
	model = FacebookPage
	template_name = 'page_delete.html'
	success_url = reverse_lazy('facebook:list_page')

class FacebookPageShow(DetailView):
	model = FacebookPage
	template_name = 'page_show.html'
