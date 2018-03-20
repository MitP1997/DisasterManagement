from django.conf.urls import url
from django.contrib import admin
from app.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^register-family/', Civilian().registerFamily),
    url(r'civilian-register/',CivilianRegistrationFormView.as_view(),name='civilian_register'),
    url(r'system-user-register/(?P<role>[a-z]+)/$',SystemUserRegistrationFormView.as_view(),name='system_user_register'),
]
