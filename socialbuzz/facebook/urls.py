from django.conf.urls import url
from .views import FacebookPageCreate, FacebookPageList, FacebookPageDelete, FacebookPageUpdate,FacebookPageShow

urlpatterns = [
    url(r'^new/', FacebookPageCreate.as_view(), name='new_page'),
    url(r'^list', FacebookPageList.as_view(), name='list_page'),
    url(r'^delete/(?P<pk>\d+)/$', FacebookPageDelete.as_view(), name='delete_page'),
    url(r'^update/(?P<pk>\d+)/$', FacebookPageUpdate.as_view(), name='update_page'),
    url(r'^show/(?P<pk>\d+)/$', FacebookPageShow.as_view(), name='show_page'),
    #url(r'^search/$', search, name='search_page'),
]
