# Create your views here.
#-*-coding:utf-8
from django.http import HttpResponse
from django.contrib.flatpages.views import flatpage
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from verify.forms import CaseForm
from verify.method import runCase
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response
from verify.models import Job
from verify.models import IncludeResult
from verify.models import Case
from verify.forms import CaseForm
from django.template import RequestContext 


def HomeView(request):
	return render_to_response("daohang.html")

@never_cache
def JobView(request):
	jobid=request.GET.get('jobid',None)
	if jobid==None:
		jobs=Job.objects.all().order_by("-id")[0:10]
	else:
		jobs=Job.objects.filter(id=jobid)
	return render_to_response("job.html",{"jobs":jobs})

def RunJobView(request):
	jobid=runCase()
	return HttpResponseRedirect("/verify/job/?jobid={0}".format(jobid))

def ResultView(request):
	jobid=request.GET.get('jobid',None)
	if jobid==None:
		results=IncludeResult.objects.all().order_by("-jobid")[0:10]
	else:
		results=IncludeResult.objects.filter(jobid=jobid)
	return render_to_response("result.html",{"results":results})


def CaseView(request):
	cases=Case.objects.all().order_by("-id")
	return render_to_response("case.html",{"cases":cases})


def EditCaseView(request,caseid):
	case=Case.objects.get(id=caseid)
	if request.method=="GET":
		caseform=CaseForm(instance=case)
		return render_to_response("editform.html",{"caseform":caseform},context_instance=RequestContext(request))
	else:
		caseform=CaseForm(request.POST,instance=case)
		caseform.save()
		return render_to_response("editform.html",{"caseform":caseform,"status":"修改成功!"},context_instance=RequestContext(request))

def AddCaseView(request):
	if request.method=="POST":
		caseform=CaseForm(request.POST)
		caseform.save()
		return HttpResponseRedirect("/verify/case/")
	else:
		caseform=CaseForm()
		return render_to_response("editform.html",{"caseform":caseform},context_instance=RequestContext(request))

def DelCaseView(request,caseid):
	case=Case.objects.get(id=caseid)
	case.delete()
	return HttpResponseRedirect("/verify/case/")







