from gps_reader.models import Activity
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from xml.etree import ElementTree as ET
from datetime import datetime
from time import strftime, gmtime
import os

def index(request):
    return render_to_response('gps_reader/index.html',
                               context_instance=RequestContext(request))

def detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.time = strftime('%H:%M:%S', gmtime(activity.time_s))
    activity.miles = activity.distance_m / 1609.344

    return render_to_response('gps_reader/detail.html', {'activity': activity})

def upload(request):
    activity = request.POST['activity']
    fn, ext = os.path.splitext(request.FILES['gpsfile'].name)

    sport = ''
    time_s = 0
    distance_m = 0
    date = ''

    if ext == '.tcx':
        sport,time_s,distance_m,date =  parse_tcx(request.FILES['gpsfile'])
    elif ext == '.gpx':
        sport,time_s,distance_m,date = parse_gpx(request.FILES['gpsfile']) 
       # return HttpResponse(distance_m)
    else:
        return HttpResponse("WHAT")
    
    act = Activity( activity = activity,
                    sport = sport,
                    time_s = time_s,
                    distance_m = distance_m,
                    date = date,
                  )
    act.save()
    return HttpResponseRedirect(reverse('activityDetail',args=(act.id,)))

def parse_tcx(file):
    tree = ET.parse(file);
    root = tree.getroot()
    namespace = root.tag[1:].split("}")[0]

    activity = root.find("{%s}Activities/{%s}Activity" % (namespace, namespace))
    sport = activity.attrib.get('Sport')
    date = activity.find("{%s}Id" % namespace).text 
    time_s = 0
    distance_m = 0

    for time in activity.findall("{%s}Lap/{%s}TotalTimeSeconds"
                                     % (namespace,namespace)):
        time_s += float(time.text)

    for distance in activity.findall("{%s}Lap/{%s}DistanceMeters" 
                                     % (namespace,namespace)):
        distance_m += float(distance.text)

    return sport,time_s,distance_m,date

def parse_gpx(file):
    tree = ET.parse(file)
    root = tree.getroot()
    namespace = root.tag[1:].split("}")[0]

    sport = 'Running'
    date = root.find("{%s}trk/{%s}name" % (namespace, namespace)).text

    end_time = '' 

    for time in root.findall("{%s}trk/{%s}trkseg/{%s}trkpt/{%s}time"
                             % (namespace, namespace, namespace, namespace)):
        end_time = time.text 

    # Handle total time
    start_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
    delta = end_time - start_time 
    time_s = delta.seconds + delta.microseconds/1E6

    return sport,time_s,0,date
