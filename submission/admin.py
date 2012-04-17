# Author Ednha
from django.contrib import admin
import settings
from submission.models import Submission,Comments,TopicArea
from submission.forms import SubmissionForm,CommentsForm
from django.contrib.contenttypes import generic


class SubmissionAdmin(admin.ModelAdmin):
  form = SubmissionForm
  exclude = ('authors','reviewers','status','comments',)

  list_display = ['title','abstract','displayStatus','displayTopics','displayPaper',]

  def get_readonly_fields(self, request, obj=None):
    if request.user.profile.type == 'Reviewer':
        return ['abstract','title','topic','paper']
    else:
        return []

  def get_urls(self):
    urls = super(SubmissionAdmin, self).get_urls()
    print urls
    return urls
  def queryset(self , request):
    qs = super(SubmissionAdmin , self).queryset(request)
    if request.user.is_superuser or request.user.profile.type == 'Reviewer':
        return qs
    return qs.filter(authors = request.user)
  def save_model(self,request,obj,form,change):
      if getattr(obj,'author',None) is None:
        obj.save()
        obj.authors.add(request.user)
        obj.last_modified_by = request.user
        obj.save()
  def get_actions(self, request):
    actions = super(SubmissionAdmin, self).get_actions(request)
    if request.user.is_superuser:
      return actions
    if request.user.profile.type == 'Author':
      del actions['accept']
      del actions['reject']
    else:
      del actions['delete_selected']
    return actions
  actions = ['accept','reject']
  def reject(self, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message_bit = "1 Submission was"
    else:
        message_bit = "%s Submissions were" % rows_updated
    self.message_user(request, "%s rejected." % message_bit)
  reject.short_description = "Mark selected as rejected"

  def accept(self, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = "1 Submission was"
    else:
        message_bit = "%s Submissions were" % rows_updated
    self.message_user(request, "%s accepted." % message_bit)
  accept.short_description = "Mark selected as accepted"

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
      return '<span style="color:green;font-size:14px;font-weight:bold">Accepted</span>'
    else:
      return '<span style="color:red;font-size:14px;font-weight:bold">Rejected</span>'
  displayStatus.short_description = 'Status'
  displayStatus.allow_tags = True


class CommentsAdmin(admin.ModelAdmin):
  pass
class TopicAreaAdmin(admin.ModelAdmin):
  pass

admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(TopicArea,TopicAreaAdmin)