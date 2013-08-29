from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('verify.views',
    # Examples:
    url(r'^home/$','HomeView'),
    url(r'^job/$','JobView'),
    url(r'^job/run/$','RunJobView'),
    url(r'^result/$','ResultView'),
    url(r'^case/$','CaseView'),
    url(r'^case/(?P<caseid>\d+)/$','EditCaseView'),
    url(r'^case/(?P<caseid>\d+)/delete/$','DelCaseView'),
    url(r'^case/add/$','AddCaseView'),
)
