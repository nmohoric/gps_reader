from gps_reader.models import Activity
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('gps_reader/index.html')

def detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render_to_response('gps_reader/detail.html', {'activity': activity})
