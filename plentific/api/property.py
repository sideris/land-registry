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
    return json_response(response)


@api_view(['GET'])
def get_properties(request):
    response = []
    request_params = request.GET

    return json_response(response)
