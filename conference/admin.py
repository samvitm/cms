# Author Ednha
from django.contrib import admin
from conference.models import *

class ProgramAdmin(admin.ModelAdmin):
  pass
class ConferenceAdmin(admin.ModelAdmin):
  pass
class LectureAdmin(admin.ModelAdmin):
  pass

admin.site.register(Program,ProgramAdmin)
admin.site.register(Conference,ConferenceAdmin)
admin.site.register(Lecture,LectureAdmin)
  