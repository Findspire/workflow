from django.conf.urls import patterns, url, include
from workflow.apps.API import views


urlpatterns = patterns('workflow.apps.API',
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^comments/(?P<item_pk>[0-9]+)/$', views.CommentList.as_view(), name='comments-list'),
    url(r'^item/(?P<item_pk>[0-9]+)/$', views.ItemDetails.as_view(), name='item-details'),
    url(r'^workflow/(?P<workflow_pk>[0-9]+)/$', views.WorkflowDetails.as_view(), name='workflow-details'),
)
