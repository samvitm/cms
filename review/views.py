from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from registration.models import UserProfile# Create your views here.
from cms.submission.models import Submission

@csrf_protect
@login_required
def assignReviewers(request,subid=None):
  if not request.user.is_superuser : raise Http404
  subs = Submission.objects.all()
  if request.POST:
    print request.POST
    rs = map(int,request.POST.getlist('reviewers'))
    sub = Submission.objects.get(pk = subid)
    for r in rs:
      print r
      sub.reviewers.add(User.objects.get(pk = r))
    sub.save()
    return render_to_response('assign.html',{'subs':subs},context_instance=RequestContext(request))
  elif subid :
    sub = Submission.objects.get(pk = subid)
    if request.GET.has_key('remove'):
      try:
        sub.reviewers.remove(User.objects.get(pk = request.GET['remove']))
        sub.save()
      except :
        pass
      return render_to_response('assign.html',{'subs':subs},context_instance=RequestContext(request))
    revs = User.objects.filter(userprofile__type = 'Reviewer')
    return render_to_response('assign.html',{'revs':revs,'sub':sub},context_instance=RequestContext(request))
  return render_to_response('assign.html',{'subs':subs},context_instance=RequestContext(request))



