# Author Ednha
from django.contrib import admin
from review.models import *

class ReviewAdmin(admin.ModelAdmin):
  pass
class ReviewUploadAdmin(admin.ModelAdmin):
  pass
class BidAdmin(admin.ModelAdmin):
  pass
class RecomendationAdmin(admin.ModelAdmin):
  pass

admin.site.register(Review,ReviewAdmin)
admin.site.register(Recomendation,RecomendationAdmin)
admin.site.register(ReviewUpload,ReviewUploadAdmin)
admin.site.register(Bid,BidAdmin)