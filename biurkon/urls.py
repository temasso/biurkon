#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from konferencje.views import KonferencjeListView, KonferencjaDetailView, SesjaDetailView
#, DzienDetailView, zgloszenie_add

from django.contrib import admin

admin.autodiscover()
from registration.backends.default.views import RegistrationView
#zmiana z simple na default!!
from last_name.forms import CustomEmailRegistrationForm


urlpatterns = patterns('',
    url(r'^$', 'biurkon.views.index', name='main_index'),                                   
    url(r'^admin/', include(admin.site.urls)),
  
    url(r'^konferencje/$', KonferencjeListView.as_view(),name='konfs' ),
    url(r'^konferencja/(?P<pk>\d+)/$', KonferencjaDetailView.as_view()),
    url(r'^konferencja/(?P<konferencja_pk>\d+)/sesja/(?P<pk>\d+)/$',SesjaDetailView.as_view()),
    url(r'^konferencje/', include('konferencje.urls')),

    url(
        r'^konta/register/$',
        RegistrationView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomEmailRegistrationForm,
            get_success_url=getattr(
                settings,
                'REGISTRATION_EMAIL_REGISTER_SUCCESS_URL',
                lambda request, user: '/'),
         ),
        name='registration_register',
    ),

    url(r'^konta/', include('registration_email.backends.default.urls')),
    url(r'^api/',include('reston.urls')) ,
    
)

if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )