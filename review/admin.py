# Author Ednha
from django.contrib import admin
from review.models import *
from review.forms import ReviewForm
class ReviewAdmin(admin.ModelAdmin):
  form = ReviewForm
  exclude = ('reviewer','comments',)
  list_display = ['submission','recomendation','overall_rating','completed',]
  list_filter = ['completed','overall_rating']
  def save_model(self,request,obj,form,change):
    obj.reviewer = request.user
    obj.last_modified_by = request.user
    obj.save()
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "submission":
        kwargs["queryset"] = Submission.objects.filter(reviewers = request.user)
    return super(ReviewAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ReviewUploadAdmin(admin.ModelAdmin):
  list_filter = ('review__completed',)
  list_display = ('submission','overall_rating','recomendation','completed',)
  def submission(self,r):
    return str(r.review.submission)
  def overall_rating(self,r):
    return str(r.review.overall_rating)
  def recomendation(self,r):
    return str(r.review.recomendation)
  def completed(self,r):
    return str(r.review.completed)


class BidAdmin(admin.ModelAdmin):
  list_display = ['submission','bid']
  list_filter = ['bid']
class RecomendationAdmin(admin.ModelAdmin):
  pass

admin.site.register(Review,ReviewAdmin)
#admin.site.register(Recomendation,RecomendationAdmin)
admin.site.register(ReviewUpload,ReviewUploadAdmin)
admin.site.register(Bid,BidAdmin)