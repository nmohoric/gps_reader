from gps_reader.models import Activity
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from xml.etree import ElementTree as ET

def index(request):
    return render_to_response('gps_reader/index.html',
                               context_instance=RequestContext(request))

def detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render_to_response('gps_reader/detail.html', {'activity': activity})

def upload(request):
    sport,time_s,distance_m,date = parse_xml(request.FILES['gpsfile'])
    return HttpResponse(', '.join([sport,time_s,distance_m,date]))

def parse_xml(file):
    tree = ET.parse(file);
    root = tree.getroot()
    namespace = root.tag[1:].split("}")[0]

    activity = root.find("{%s}Activities/{%s}Activity" % (namespace, namespace))
    sport = activity.attrib.get('Sport')
    date = activity.find("{%s}Id" % namespace).text 
    time_s = 0
    distance_m = 0

    for lap in activity.iter("{%s}Lap" % namespace):
        for node in lap.iter():
            if node.tag == ("{%s}TotalTimeSeconds" % namespace):
                time_s += float(node.text)
            if node.tag == ("{%s}DistanceMeters" % namespace):
                distance_m += float(node.text)

    return sport,str(time_s),str(distance_m),date
