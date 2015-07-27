#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.utils.decorators import method_decorator


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
    template_name_suffix = '_form'
    template_name = 'team/views_generic_form.haml'

    def get_context_data(self, **kwargs):
        context = super(CreateUpdateView, self).get_context_data(**kwargs)
        context.update({
            'submit': 'Update' if self.is_update_request() else 'Create',
        })
        context.update(self.get_bonus_context_data())
        return context

    def get_bonus_context_data(self):
        return {}

    def get_success_url(self):
        return reverse('team:index')


class LoginRequiredMixin(object):
    """Ensures that user must be authenticated in order to access the view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
