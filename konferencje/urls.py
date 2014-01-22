from django.conf.urls import patterns, url
from konferencje import views


urlpatterns = patterns('',

    url(r'^zgloszenia/', views.TwojeZgloszenia, name='TwojeZgloszenia'),
    url(r'^zgloszenie/(?P<konferencja_pk>\d+)/$', views.zgloszenie_add, name='zgloszenie'),
    url(r'^pdf/(?P<sesja_pk>\d+)/$', views.sesja_pdf, name='pdf'),

)