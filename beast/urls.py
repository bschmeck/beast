from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Examples:
    url(r'^$', 'workouts.views.calendar'),
    url(r'^workout/(?P<w_id>\d+)/$', 'workouts.views.getWorkout'),
    url(r'^workout/(?P<w_id>\d+)/action/$', 'workouts.views.joinWorkout'),
    url(r'^workout/(?P<w_id>\d+)/delete/$', 'workouts.views.deleteWorkout'),
    url(r'^workout/(?P<w_id>\d+)/update/$', 'workouts.views.updateWorkout'),
    url(r'^workout/create/$', 'workouts.views.createWorkout'),
    (r'^account/$', 'workouts.views.account'),
    (r'^account/login/$', 'django.contrib.auth.views.login'),
    (r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^account/update/$', 'workouts.views.account'),
    (r'^account/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect': '/account/password/reset/done/'}),
    (r'^account/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^account/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': '/account/password/done/'}),
    (r'^account/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^account/register/$', 'workouts.views.accountCreate'),
    (r'^faq$', 'workouts.views.faq'),
)
