from django.db.models import Max, Min
from django.http import HttpResponse
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
        "postcodes" : Property.postcodes
    }
    return json_response(response)


@api_view(['GET'])
def get_property_list_date_location(request):
    params = request.GET
    pc          = params.get('postcode', None)  # support only postcodes for now
    from_date   = params.get('from', None)
    to_date     = params.get('to', None)
    if not (pc or from_date or to_date):
        return HttpResponse(status=418)

    result = Property.list_filtered(pc, {'min': from_date, 'max': to_date})
    print result
    return json_response(result)
