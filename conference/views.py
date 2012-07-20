# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from cms.conference.forms import *
from django.contrib import messages
from cms.conference.models import Conference

@login_required
@csrf_protect
def pay(request):
  form = PaymentForm()
  payments = Payment.objects.filter(payment_from=request.user)
  if request.POST:
    form = PaymentForm(request.POST)
    if form.is_valid():
      p = form.save(commit=False)
      p.payment_from = request.user
      p.save()
      import hashlib
      p.transaction_id = hashlib.sha384(str(p.id)).hexdigest()[:9]
      p.save()
      messages.success(request,'Payment Made successfully! You will be notified when your payment is verified by the authorities')
      form = PaymentForm()
      return render_to_response('payment.html',{'form':form,'payments':payments},context_instance=RequestContext(request))
    else:
      messages.error(request,'Please correct the errors below')
      return render_to_response('payment.html',{'form':form,'payments':payments},context_instance=RequestContext(request))
  return render_to_response('payment.html',{'form':form,'payments':payments},context_instance=RequestContext(request))


def invite(request):
  if request.POST:
    if request.POST['to'] == '' or request.POST['subject'] == '' or request.POST['text'] == '':
      messages.error(request,'Some fields have been left blank. Please fill them')
      return render_to_response('invite.html',context_instance=RequestContext(request))
    emails = str(request.POST['to']).split(',')
    bcc_list = emails
    while len(bcc_list):
      connection = mail.get_connection()
      connection.open()
      email = EmailMultiAlternatives(request.POST['subject'], request.POST['text'], 'BITS Conference <noreply@bits-cms.mailgun.com>',
                [''],bcc_list[:200],
                )
      connection.send_messages([email])
      bcc_list = bcc_list[200:]
      connection.close()
      messages.success(request,'Emails sent!')
    return render_to_response('invite.html',context_instance=RequestContext(request))
  return render_to_response('invite.html',context_instance=RequestContext(request))


def conference(request):
  confs = Conference.objects.all()
  return render_to_response('conferences.html',locals(),context_instance=RequestContext(request))

def about(request):
  return render_to_response('about.html',locals(),context_instance=RequestContext(request))

def contact(request):
  return render_to_response('contact.html',locals(),context_instance=RequestContext(request))