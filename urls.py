from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cms.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$','django.views.static.serve',
         {'document_root':'static/files/'}),
)

urlpatterns+=patterns('cms.registration.views',

  url(r'^signup/$','signup',name='signup'),
  url(r'^login/$','login',name='login'),
)
