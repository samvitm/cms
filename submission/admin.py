# Author Ednha
from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
import cms.settings
from cms.submission.models import Submission,Comments,TopicArea, Author
from cms.submission.forms import SubmissionForm,CommentsForm
from django.contrib.contenttypes import generic

class CommentsInline(admin.StackedInline):
  model = Comments
  extra = 1
  exclude = ('author',)
 

class AuthorInline(admin.StackedInline):
  model = Author
  extra = 1


class SubmissionAdmin(admin.ModelAdmin):
  form = SubmissionForm
  inlines = [AuthorInline]
  exclude = ('author','reviewers','status',)
  def change_view(self, request, obj_id):
    if request.user.profile.type=='Reviewer':
      self.inline_instances = []
    else:
      pass
    return super(SubmissionAdmin, self).change_view(request, obj_id)

  def add_view(self, request):
    if request.user.profile.type=='Reviewer':
      print self
      self.inline_instances = []
    else:
      pass
    return super(SubmissionAdmin, self).add_view(request)

  list_display = ['title','abstract','displayStatus','displayTopics','displayPaper',]

  def get_readonly_fields(self, request, obj=None):
    if request.user.profile.type == 'Reviewer':
        return ['abstract','title','topic','paper']
    else:
        return []

  def get_urls(self):
    urls = super(SubmissionAdmin, self).get_urls()
    return urls
  def queryset(self , request):
    qs = super(SubmissionAdmin , self).queryset(request)
    if request.user.is_superuser or request.user.profile.type == 'Reviewer':
        return qs
    return qs.filter(author = request.user)
  def save_formset(self, request, form, formset, change):
    comments = formset.save(commit=False)
    for c in comments:
      c.author = request.user
      c.save()
  def save_model(self,request,obj,form,change):
    print 'save_model _submission'
    obj.author = request.user
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
    for sub in queryset:
        email = render_to_string('emails/statusacc.html',{'sub':sub})
        send_mail('Your paper has been accepted  ',email,'BITS Conference <noreply@bits-cms.mailgun.com>',[sub.author.email],fail_silently = True)
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
    link = '<ul>'
    link += '<li><a href="%spaper_uploads/%s">Download</a></li>' % (cms.settings.MEDIA_URL,p,)
    link +='<li><a href="/comments?s='+str(sub.id)+'">Comment / View Comments</a></li>'
    link += '</ul>'
    return link
  displayPaper.short_description = 'Manage'
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
  def save_formset(self, request, form, formset, change):
    print 'formsetsave'
  def save_model(self, request, obj, form, change):
    print 'jerer'

class TopicAreaAdmin(admin.ModelAdmin):
  pass

admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(TopicArea,TopicAreaAdmin)