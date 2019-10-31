from .version import Version
from django.shortcuts import HttpResponse
import json

#设置版本信息
def request_set_version(request):
    app_id = request.GET.get("appid")
    version = request.GET.get("version")
    release_note = request.GET.get("note")
    date = request.GET.get("date")

    version_obj = Version()
    version_obj.set_version(app_id, version, release_note, date)
    json_data = json.dumps(version_obj.retrun_obj.__dict__)
    return HttpResponse(json_data, content_type="application/json")

def request_get_version(request):
    app_id = request.GET.get("appid")
    user_id = request.GET.get("userid")

    version_obj = Version()
    version_obj.get_version(app_id, user_id)
    json_data = json.dumps(version_obj.retrun_obj.__dict__)
    return HttpResponse(json_data, content_type="application/json")