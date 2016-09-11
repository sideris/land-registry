from rest_framework.decorators import api_view

from plentific.api.utils import json_response


@api_view(['GET'])
def setup_app(request):
    response = {
        "date_limits": [],
        "postcodes"  : []
    }
    return json_response(response)
