from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from cms.registration.froms import SignUpForm
from django.contrib.auth import authenticate
from registration.models import UserProfile


@csrf_protect
def signup(request):
  form = SignUpForm()
  if request.POST:
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.is_staff = True
      profile = UserProfile()
      profile.phone_number = form.cleaned_data['phone']
      profile.city = form.cleaned_data['city']
      profile.country = form.cleaned_data['country']
      profile.type = form.cleaned_data['type']
      profile.user = user
      profile.save()
      if profile.type == 'Author':
        user.groups.add(Group.objects.get_or_create(name='Authors')[0])
      if profile.type == 'Reviewer':
        user.groups.add(Group.objects.get_or_create(name='Reviewer')[0])
      if profile.type == 'ConfAdmin':
        user.groups.add(Group.objects.get_or_create(name='Conference Admin')[0])
      if profile.type == 'Delegate':
        user.groups.add(Group.objects.get_or_create(name='Delegate')[0])
      if profile.type == 'Sponsor':
        user.groups.add(Group.objects.get_or_create(name='Sponsor')[0])
      user.save()
      u = authenticate(username = user.username,password = form.cleaned_data['password'])
      auth.login(request,u)
      return HttpResponseRedirect(reverse('admin:index'))
      #message = 'Some error has occurred!'
      #return render_to_response('signup.html',{'form':form,'message':message},context_instance=RequestContext(request))
  return render_to_response('signup.html',{'form':form},context_instance=RequestContext(request))


@csrf_protect
def login(request):
  form = SignUpForm()
  if request.user.is_authenticated() :
    return HttpResponseRedirect(reverse('admin:index'))
  if request.POST :
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username = username,password = password)
    if user is not None and user.is_active:
        auth.login(request,user)
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        message = 'Username does not exist/Wrong username-password!'
        return render_to_response('signup.html', {'form':form,'lmessage':message},context_instance=RequestContext(request))
  return render_to_response('signup.html', {'form':form},context_instance=RequestContext(request))
