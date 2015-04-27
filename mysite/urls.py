from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    url(r'^polls/', include('polls.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mysite.views.first_page'),(r'^site_medias/(?P<path>.*)$','django.views.static.serve',
        {'document_root':'mysite/static', 'show_indexes': True}),
    url(r'^hello','mysite.views.hello'),
    url(r'^hey','mysite.views.returnDic'),


#user
     url(r'^register','mysite.user.register'),
     url(r'^login','mysite.user.login'),
     url(r'^logout','mysite.user.login'),
     url(r'^changePaswd','mysite.user.changePaswd'),
     url(r'^history','mysite.user.history'),
     url(r'^order','mysite.user.order'),
     url(r'^cancelOrder','mysite.user.cancelOrder'),
#respository
     url(r'^repository','mysite.respository.get_report'),
     url(r'^funds','mysite.respository.get_finance'),
     url(r'^trade','mysite.respository.trade'),
     url(r'^detail','mysite.detail.get'),
     url(r'^news','mysite.detail.news'),
     url(r'^olddetail','mysite.detail.old')

)

# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

