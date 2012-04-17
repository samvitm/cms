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

admin.site.register(Program,ProgramAdmin)
admin.site.register(Conference,ConferenceAdmin)
admin.site.register(Lecture,LectureAdmin)
  