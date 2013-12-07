# Create your views here.
import models
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext


def home(request):
    return render_to_response("home.html",
                              {},
                              context_instance=RequestContext(request))


