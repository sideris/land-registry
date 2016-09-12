from django.db.models import Max, Min
from django.views.decorators.gzip import gzip_page
from rest_framework.decorators import api_view

from plentific.api.utils import json_response
from properties.models import Property, Transaction


# @gzip_page
@api_view(['GET'])
def setup_app(request):
    response = {
        "date_limits" : [
            Transaction.objects.all().aggregate(Min('transfer_date'))["transfer_date__min"],
            Transaction.objects.all().aggregate(Max('transfer_date'))["transfer_date__max"]
        ],
        "postcodes" : map(lambda x: x['post_code'], Property.objects.values('post_code').distinct())
    }
    # for pc in response['postcodes']:
    #     r = Property.objects.filter(post_code=pc).all()
    #     if len(r)> 10:
    #         print len(r), pc
    return json_response(response)


@api_view(['GET'])
def get_property_counts(request):
    response = []
    request_params = request.GET # get the params from here
    a = Property.list_filtered('LONDON', {'min': '2001-01-01', 'max': '2016-02-01'})
    for p in a:
        response.extend(map(lambda x: x['transfer_date'], p['transactions']))
        print
    response.sort()
    return json_response(response)
