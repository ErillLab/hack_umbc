# Create your views here.
import models
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext


def home(request):
    all_courses = models.Course.objects.filter(section__yr=2012,
                                               section__semester='Fall')
    return render_to_response("home.html",
                              {'courses': all_courses},
                              context_instance=RequestContext(request))

def list_all_courses(request):
    all_courses = models.Course.objects.all()
    return render_to_response("list_all_courses.html",
                              {'courses': all_courses},
                              context_instance=RequestContext(request))




