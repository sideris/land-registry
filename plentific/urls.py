"""plentific URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from plentific.api.property import get_property_list_date_location, postcode_suggest
from properties.views import View

urlpatterns = [
    # url(r'^$',          View.as_view(template_name="../templates/base.html"), name='home'),
    url(r'^ts/',        View.as_view(template_name="../templates/timeseries.html", name="timeseries",
                                     title='Timeseries'), name=''),
    url(r'^brackets/',  View.as_view(template_name="../templates/price_brackets.html",
                                     name="price_brackets", title='Price brackets'), name=''),

    url(r'^postcode/(?P<search_term>.*?)/$',    postcode_suggest),
    url(r'^properties',                        get_property_list_date_location)
]
