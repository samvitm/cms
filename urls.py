from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'cms.views.home', name='home'),
    (r'^media/(?P<path>.*)$','django.views.static.serve',
         {'document_root':'/static/files/'}),
)

urlpatterns+=patterns('cms.registration.views',

  url(r'^signup/$','signup',name='signup'),
  url(r'^login/$','login',name='login'),
)

urlpatterns+=patterns('cms.review.views',

  url(r'^assign/(?P<subid>\d+)?$','assignReviewers',name='assign'),

)

urlpatterns+=patterns('cms.submission.views',

  url(r'^comments/$','comment',name='comment'),

)

urlpatterns+=patterns('cms.conference.views',

  url(r'^pay/$','pay',name='pay'),
  url(r'^invite/$','invite',name='invite'),
  url(r'^conferences/$','conference',name='conferences'),
  url(r'^about/$','about',name='about'),
  url(r'^contact/$','contact',name='contact'),

  url(r'^', include(admin.site.urls),name='admin'),

)



