from django.conf.urls import url
from django.contrib import admin
from app.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register-family/', Civilian().registerFamily),
    url(r'^admin_home/$', AdminHome.as_view(), name='admin-home'),
    url(r'^admin_supplier/$', AdminSuppliers.as_view(), name='supplier-details'),
    url(r'^admin_officials/$', AdminOfficals.as_view(), name='official-details'),
    url(r'^admin_civilians/$', AdminCivilians.as_view(), name='civilian-home'),
    url(r'^entrydata/', shelderadd, name='entrypoint'),
 	url(r'^admin_shelter/(?P<pk>\d+)/$', AdminShelter.as_view(), name='shelter-details'),
       
]
