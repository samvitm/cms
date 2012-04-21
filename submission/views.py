# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from cms.submission.models import Submission,Comments

@csrf_protect
@login_required
def comment(request):
  if request.GET.has_key('s') or request.POST.has_key('sub'):
    try:
      s = request.GET['s']
    except :
      s = request.POST['sub']
    sub = Submission.objects.get(pk = int(s))
    if not request.user.is_superuser:
      if sub.author != request.user and (long(request.user.id),) not  in sub.reviewers.values_list('id'):
        raise Http404
  else:
    raise Http404
  if request.POST:
    ct = request.POST['comment']
    c = Comments()
    c.comment = ct
    c.author = request.user
    c.submission  = sub
    c.save()

  coms = sub.sub.all().order_by('time')
  return render_to_response('comment.html',{'sub':sub,'coms':coms},context_instance=RequestContext(request))