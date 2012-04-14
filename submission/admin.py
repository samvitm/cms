# Author Ednha
from django.contrib import admin
from submission.models import Submission,Comments,TopicArea

class SubmissionAdmin(admin.ModelAdmin):
  pass
class CommentsAdmin(admin.ModelAdmin):
  pass
class TopicAreaAdmin(admin.ModelAdmin):
  pass

admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(TopicArea,TopicAreaAdmin)