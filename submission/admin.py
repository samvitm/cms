# Author Ednha
from django.contrib import admin
import settings
from submission.models import Submission,Comments,TopicArea
from submission.forms import SubmissionForm,CommentsForm
from django.contrib.contenttypes import generic


class SubmissionAdmin(admin.ModelAdmin):
  form = SubmissionForm
  exclude = ('authors','reviewers','status','comments',)

  list_display = ['title','displayStatus','displayTopics','displayPaper',]
  def get_urls(self):
    urls = super(SubmissionAdmin, self).get_urls()
    print urls
    return urls
  def queryset(self , request):
    qs = super(SubmissionAdmin , self).queryset(request)
    if request.user.is_superuser:
        return qs
    return qs.filter(authors = request.user)
  def save_model(self,request,obj,form,change):
      if getattr(obj,'author',None) is None:
        obj.save()
        obj.authors.add(request.user)
        obj.last_modified_by = request.user
        obj.save()

  def displayTopics(self,sub):
    cs = sub.topic.all()
    s = '<ul class="radiolist">'
    for c in cs:
      s+='<li>'+str(c)+'</li>'
    s+='</ul>'
    return s
  displayTopics.short_description = 'Topic areas'
  displayTopics.allow_tags = True

  def displayPaper(self,sub):
    p = str(sub.paper).split('/')[-1]
    link = '<a href="%spaper_uploads/%s">Download</a>' % (settings.MEDIA_URL,p,)
    return link
  displayPaper.short_description = 'Download Paper'
  displayPaper.allow_tags = True

  def displayStatus(self,sub):
    if sub.status is None:
      return 'Undecided'
    elif sub.status == True:
      return 'Accepted'
    else:
      return 'Rejected'
  displayStatus.short_description = 'Status'


class CommentsAdmin(admin.ModelAdmin):
  pass
class TopicAreaAdmin(admin.ModelAdmin):
  pass

admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(TopicArea,TopicAreaAdmin)