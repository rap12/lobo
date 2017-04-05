"""reservation_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from cinema import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_view),
    url(r'^login/$', views.login_view),
    url(r'^register/$', views.register_view),
    url(r'^register_form/$', views.register_form),
    url(r'^login_form/$', views.login_form),
    url(r'^logout/$', views.log_out),
    url(r'^films/$', views.films_view),
    url(r'^program/$', views.program_view),
    url(r'^book_tickets/$', views.book_tickets),
    url(r'^program/movie(?P<num>[0-9]+)/$', views.movie_showtime),
    url(r'^book(?P<num>[0-9]+)/$', views.book_seats),
    url(r'^contact/$', views.contact_view),
    url(r'^administration/$', views.admin_view),
    url(r'^administration_time/$', views.admin_time_view),
    url(r'^administration_add_movie/$', views.admin_add_movie_view),
    url(r'^administration_add_showtime/$', views.admin_add_showtime_view),
    url(r'^administration_showtime_data/$', views.admin_showtime_data_view),
    url(r'^administration_add_auditorium/$', views.admin_add_auditorium_view),
    url(r'^reservation/$', views.reservation_view),
    url(r'^ticket_reservation(?P<num>[0-9]+)/$', views.get_reservation_ticket),
    url(r'^ticket_new/$', views.get_ticket),
    url(r'^client_reservation/$', views.client_reservation),
]

