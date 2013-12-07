# Create your views here.
import models
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
import json

def home(request):
    all_courses = models.Course.objects.filter(section__yr=2012,
                                               section__semester='Fall').distinct()
    return render_to_response("home.html",
                              {'courses': all_courses},
                              context_instance=RequestContext(request))

def list_all_courses(request):
    all_courses = models.Course.objects.all()
    return render_to_response("list_all_courses.html",
                              {'courses': all_courses},
                              context_instance=RequestContext(request))


def get_section_info_ajax(request, uid):
    #uid = request.POST['uid']
    section = models.Section.objects.get(courseid=uid)
    json_resp = {}
    json_resp['course-number'] = section.course.dept + section.course.number
    json_resp['course-title'] = section.course.title
    json_resp['course-description'] = section.course.description
    json_resp['instructor'] = section.professor.name
    json_resp['semester'] = section.semester
    json_resp['approachableness'] = section.evaluation.approachableness
    json_resp['fairness'] = section.evaluation.fairness
    json_resp['engagingness'] = section.evaluation.engagingness
    json_resp['sessions'] = [{'time-start-hr': ses.time_start_hr,
                              'time-start-min': ses.time_start_min,
                              'time-end-hr': ses.time_end_hr,
                              'time-end-min': ses.time_end_min}
                             for ses in section.sessions_set.all()}]

    
    return HttpResponse(json.dumps(json_resp), mimetype="application/json")

