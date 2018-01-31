from django.conf.urls import url
from .views import HomeView, FacebookPageSearch, FacebookPostSearch, FacebookPostList, FacebookCommentList, FacebookPageDelete, FacebookPostDelete, FacebookPageUpdate, FacebookPageShow, FacebookPostShow

urlpatterns = [
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^new_page/', FacebookPageSearch.as_view(), name='new_page'),
    url(r'^new_post/', FacebookPostSearch.as_view(), name='new_post'),
    url(r'^pages', FacebookPostList.as_view(), name='list_post'),
    url(r'^posts', FacebookCommentList.as_view(), name='list_comment'),
    url(r'^delete_page/(?P<pk>\d+)/$', FacebookPageDelete.as_view(), name='delete_page'),
    url(r'^delete_post/(?P<pk>\d+)/$', FacebookPostDelete.as_view(), name='delete_post'),
    url(r'^update/(?P<pk>\d+)/$', FacebookPageUpdate.as_view(), name='update_page'),
    url(r'^show_page/(?P<pk>\d+)/$', FacebookPageShow.as_view(), name='show_page'),
    url(r'^show_post/(?P<pk>\d+)/$', FacebookPostShow.as_view(), name='show_post'),
]
