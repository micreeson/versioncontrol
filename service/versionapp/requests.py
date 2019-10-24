from .version import Version
from django.shortcuts import HttpResponse
import json

def request_get_version(request):
    app_id = request.GET.get("appid")
    version = request.GET.get("version")

    version_obj = Version()
    version_obj.set_version(app_id, version)
    json_data = json.dumps(version_obj.__dict__)
    return HttpResponse(json_data, content_type="application/json")