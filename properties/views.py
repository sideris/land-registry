from __future__ import absolute_import
from django.views.generic import TemplateView


class View(TemplateView):

    name = None
    title = None

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['container_id'] = 'time_series_view'
        context['name'] = self.name
        context['title'] = 'Register - ' + self.title if self.title else 'Register'
        return context
