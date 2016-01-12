from django.conf.urls import patterns, url, include
from workflow.apps.API import views


urlpatterns = patterns('workflow.apps.API',
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^comments/(?P<item_pk>[0-9]+)/$', views.CommentList.as_view(), name='comments-list'),
    url(r'^item/(?P<item_pk>[0-9]+)/$', views.ItemDetails.as_view(), name='item-details'),
    url(r'^workflow/$', views.WorkflowList.as_view(), name='workflow-list'),
    url(r'^workflow/(?P<workflow_pk>[0-9]+)/$', views.WorkflowDetails.as_view(), name='workflow-details'),
    url(r'^projects/$', views.ProjectList.as_view(), name='projects-list'),
    url(r'^projects/(?P<project_pk>[0-9]+)/workflows/$', views.ProjectWorkflowList.as_view(), name='project-workflows'),
    url(r'^drag-workflow/(?P<workflow_pk>[0-9]+)(?:/(?P<related_pk>[0-9]+))?/$', views.WorkflowDragPosition.as_view(), name='drag_workflow'),
    url(r'^drag-item/(?P<item_pk>[0-9]+)(?:/(?P<related_pk>[0-9]+))?/$', views.ItemDragPosition.as_view(), name="drag-item"),
    url(r'^drag-category/(?P<category_pk>[0-9]+)(?:/(?P<related_pk>[0-9]+))?/$', views.CategoryDragPosition.as_view(), name="drag-category")
)
