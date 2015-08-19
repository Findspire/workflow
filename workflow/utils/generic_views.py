#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module extend the django class based views: it merges CreateView and UpdateView.

Note: Like any django class based view. LoginRequiredMixin is optional.

BaseCreateUpdateView:
    This is an internal class, like django's BaseCreateView or BaseUpdateView.
    It should not be used directly (cf. the django comments)

CreateUpdateView:
    This is used instead of the django's CreateView and UpdateView.
    It overwrites some methods :
        get_context_data: Add a few var in the template context
        get_initial: Add the param passed through the url to the initial_data used to instanciate the form.

    Usage:
        class SomeView(LoginRequiredMixin, CreateUpdateView):
            model = SomeModel
            form_class = SomeModelForm
            success_url = '/some/url/'

MyListView:
    This is used instead of the django's ListView. It add a paginator that should be included in your main
    template via the partial template 'utils/paginator.part.haml'

    class SomeView(LoginRequiredMixin, MyListView):
        # ... the standards django's ListView fields

"""

from __future__ import unicode_literals

from django.http.response import JsonResponse
from django.utils.translation import ugettext as _
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.list import ListView

from workflow.utils.paginator import paginator_range


class BaseCreateUpdateView(ModelFormMixin, ProcessFormView):
    """
    Base view for creating and updating an existing object.

    Using this base class requires subclassing to provide a response mixin.
    """

    object_url_kwargs = ['slug', 'pk']

    def get_object(self, queryset=None):
        if self.is_update_request():
            return super(BaseCreateUpdateView, self).get_object(queryset)
        else:
            return None

    def is_update_request(self):
        """
        Returns True if current request is an object update request, False if it's an object create request.

        Checks if the URL contains a parameter identifying an object.
        Possible URL parameter names are defined in self.object_url_kwargs
        """
        for object_kwarg in self.object_url_kwargs:
            if object_kwarg in self.kwargs:
                return True
        return False

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseCreateUpdateView, self).post(request, *args, **kwargs)


class CreateUpdateView(SingleObjectTemplateResponseMixin, BaseCreateUpdateView):
    """
    View for creating a new object instance or updating an existing one,
    with a response rendered by template.
    """

    def get_context_data(self, **kwargs):
        context = super(CreateUpdateView, self).get_context_data(**kwargs)

        if self.is_update_request():
            context.update({
                'title': _('%(name)s update') % {'name': self.model._meta.verbose_name.capitalize()},
                'submit': _('Update'),
            })
        else:
            context.update({
                'title': _('%(name)s creation') % {'name': self.model._meta.verbose_name.capitalize()},
                'submit': _('Save'),
            })

        return context

    def get_initial(self):
        initial = super(CreateUpdateView, self).get_initial()
        initial.update(self.kwargs)  # add the param passed by the url to the initial form data
        return initial

    def form_valid(self, form):
        ret = super(CreateUpdateView, self).form_valid(form)

        if self.request.is_ajax():
            # Send something special so the ajax call know that it is a successfull form validation
            # Ajax calls cant see the difference between a status code 302 (form success) or a 200 (form failure)
            return JsonResponse({})
        else:
            return ret


class MyListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(MyListView, self).get_context_data(**kwargs)
        context.update({
            'mypaginator': paginator_range(context['page_obj'].number, context['paginator'].num_pages)
        })
        return context
