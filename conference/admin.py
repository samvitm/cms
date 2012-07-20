# Author Ednha
from django.contrib import admin
from conference.models import *

class ProgramAdmin(admin.ModelAdmin):
  list_display = ['conference','name','venue','start_date_time','end_date_time']
  list_filter = ['conference']
class ConferenceAdmin(admin.ModelAdmin):
  list_display = ['name','start_date','end_date','venue','admin','about']
class LectureAdmin(admin.ModelAdmin):
  list_display = ['name','conference','program','description']
  list_filter = ['program','program__conference']
  def conference(self,l):
    return str(l.program.conference )

class PaymentAdmin(admin.ModelAdmin):
  list_display = ['payment_from','conference','mode','amount','transaction_id','verified']
  exclude = ('payment_from','transaction_id','verified')
  list_filter = ['conference','mode','verified','package']

  def verify(self, request, queryset):
    rows_updated = queryset.update(verified=True)
    if rows_updated == 1:
        message_bit = "1 Payment was"
    else:
        message_bit = "%s Payments were" % rows_updated
    self.message_user(request, "%s verified." % message_bit)
  verify.short_description = "Mark selected as verified"

  def invalid(self, request, queryset):
    rows_updated = queryset.update(verified=False)
    if rows_updated == 1:
        message_bit = "1 Payment was"
    else:
        message_bit = "%s Payments were" % rows_updated
    self.message_user(request, "%s marked as invalid." % message_bit)
  invalid.short_description = "Mark selected as invalid"

  actions = ['verify','invalid']

  def amount(self,p):
    return p.package.amount
  def save_model(self,request,obj,form,change):
    obj.payment_from = request.user
    obj.last_modified_by = request.user
    import hashlib
    obj.save()
    obj.transaction_id = hashlib.sha384(str(obj.id)).hexdigest()[:9]
    obj.save()


class PackageAdmin(admin.ModelAdmin):
  list_display = ['conference','includes','amount']

class AreaAdmin(admin.ModelAdmin):
  pass

class BannerAdmin(admin.ModelAdmin):
  exclude = ('author',)
  def save_model(self,request,obj,form,change):
    obj.author = request.user
    obj.last_modified_by = request.user
    obj.save()
  def queryset(self , request):
    qs = super(BannerAdmin , self).queryset(request)
    if request.user.is_superuser :
        return qs
    return qs.filter(author = request.user)

admin.site.register(Program,ProgramAdmin)
admin.site.register(Conference,ConferenceAdmin)
admin.site.register(Lecture,LectureAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Package,PackageAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Banner,BannerAdmin)
