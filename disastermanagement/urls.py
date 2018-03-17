from django.conf.urls import url
from django.contrib import admin
from app.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^register-family/', Civilian().registerFamily),
    url(r'official-register/',OfficialRegistrationFormView.as_view(),name='official_register'),
    url(r'civilian-register/',CivilianRegistrationFormView.as_view(),name='civilian_register'),
    url(r'family-register/',FamilyRegistrationFormView.as_view(),name='family_register'),
]
