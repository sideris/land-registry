from __future__ import absolute_import
from django.views.generic import TemplateView


class HomePageView(TemplateView):

    template_name = "../templates/base.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['test'] = 'hai'
        return context
