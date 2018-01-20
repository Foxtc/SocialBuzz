from django.conf.urls import url
from .views import FacebookPageSearch, FacebookPostList, FacebookCommentList, FacebookPageDelete, FacebookPageUpdate, FacebookPageShow

urlpatterns = [
    url(r'^new/', FacebookPageSearch.as_view(), name='new_search'),
    url(r'^pages', FacebookPostList.as_view(), name='list_post'),
    url(r'^posts', FacebookCommentList.as_view(), name='list_comment'),
    url(r'^delete/(?P<pk>\d+)/$', FacebookPageDelete.as_view(), name='delete'),
    url(r'^update/(?P<pk>\d+)/$', FacebookPageUpdate.as_view(), name='update'),
    url(r'^show/(?P<pk>\d+)/$', FacebookPageShow.as_view(), name='show'),
    #url(r'^search/$', search, name='search_page'),
]
