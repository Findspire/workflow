from django.conf.urls import patterns, url
from workflow.apps.API import views


urlpatterns = patterns('workflow.apps.API',
    url(r'^comments/(?P<item_pk>[0-9]+)/$', views.CommentList.as_view(), name='comments-list'),
    
)
