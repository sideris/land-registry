from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view

from plentific.api.utils import json_response
from properties.models import Property, Transaction


@api_view(['GET'])
def postcode_suggest(request, search_term=None):
    """
    Accepts a search term for a post code and returns a list of results
    :param request:
    :param search_term:
    :return:
    """
    result = []
    if search_term:
        qs = Property.objects.values('postcode').filter(Q(postcode__icontains=search_term)).distinct()
        result = map(lambda x: x['postcode'], qs)
    return json_response(result)


# @gzip_page
@api_view(['GET'])
def get_property_list_date_location(request):
    params      = request.GET
    pc          = params.get('postcode', None)  # support only postcodes for now
    from_date   = params.get('from', None)
    to_date     = params.get('to', None)
    if not (pc or from_date or to_date):
        return HttpResponse(status=418)
    result = Property.list_filtered(pc, {'min': from_date, 'max': to_date})
    return json_response(result)


@api_view(['GET'])
def date_limits(request):
    result = {'date_limits': Transaction.date_limits()}
    return json_response(result)
