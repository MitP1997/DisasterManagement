from django.conf.urls import url
from django.contrib import admin
from app.views import *
from django.contrib.auth.decorators import login_required
from app.decorators import user_is_operator

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^register-family/', Civilian().registerFamily),
    url(r'civilian-register/',CivilianRegistrationFormView.as_view(),name='civilian_register'),
    url(r'system-user-register/(?P<role>[a-z]+)/',SystemUserRegistrationFormView.as_view(),name='system_user_register'),
    url(r'login/',LoginFormView.as_view(),name='login'),
	
	url(r'^admin_home/$', AdminHome.as_view(), name='admin-home'),
    url(r'^admin_supplier/$', AdminSuppliers.as_view(), name='supplier-details'),
    url(r'^admin_officials/$', AdminOfficals.as_view(), name='official-details'),
    url(r'^admin_civilians/$', AdminCivilians.as_view(), name='civilian-home'),
    url(r'^admin_shelter/(?P<pk>\d+)/$', AdminShelter.as_view(), name='shelter-details-admin'),
    
    url(r'^official-civilians/(?P<pk>\d+)/$', OfficialCivilians.as_view(), name='civilian-shelter'),
    url(r'^official-shelter/(?P<pk>\d+)/$', OfficialShelter.as_view(), name='shelter-details-official'),
    

    url(r'register-at-shelter/',user_is_operator(login_required(RegisterAtShelterFormView.as_view())),name='register_at_shelter'),
    url(r'allocate-at-shelter/(?P<type>[a-z]+)/',user_is_operator(login_required(AllocationAtShelterFormView.as_view())),name='allocate_at_shelter'),
    url(r'make-blocks/',PreDRAPComputation.as_view(),name='pre_drap_comp'),
    url(r'compute-block-dict/',BlockDictComputation.as_view(),name='compute_block_dict'),
]
