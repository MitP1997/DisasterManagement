from django.conf.urls import url
from django.contrib import admin
from app.views import *
from app import views
from django.contrib.auth.decorators import login_required
from app.decorators import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'civilian-register/',CivilianRegistrationFormView.as_view(),name='civilian_register'),
    url(r'system-user-register/(?P<role>[a-z]+)/',SystemUserRegistrationFormView.as_view(),name='system_user_register'),
    url(r'login/',LoginFormView.as_view(),name='login'),

	url(r'^admin-home/$', user_is_admin(login_required(AdminHome.as_view())), name='admin-home'),
    url(r'^admin-supplier/$', user_is_admin(login_required(AdminSuppliers.as_view())), name='supplier-details'),
    url(r'^admin-officials/$', user_is_admin(login_required(AdminOfficals.as_view())), name='official-details'),
    url(r'^admin-civilians/$', user_is_admin(login_required(AdminCivilians.as_view())), name='civilian-home'),
    url(r'^admin-shelter/(?P<pk>\d+)/$', user_is_admin(login_required(AdminShelter.as_view())), name='shelter-details-admin'),

    url(r'^official-civilians/(?P<pk>\d+)/$', user_is_operator(login_required(OfficialCivilians.as_view())), name='civilian-shelter'),
    url(r'^official-home/(?P<pk>\d+)/$', user_is_operator(login_required(OfficialShelter.as_view())), name='shelter-details-official'),
    url(r'^official-add-civilian/(?P<pk>\d+)/$', user_is_operator(login_required(RegisterAtShelterFormView.as_view())), name='civilian-register-shelter'),
    url(r'allocate-at-shelter/(?P<pk>\d+)/(?P<type>[a-z]+)/',user_is_operator(login_required(AllocationAtShelterFormView.as_view())),name='allocate_at_shelter'),

    url(r'register-at-shelter/',user_is_operator(login_required(RegisterAtShelterFormView.as_view())),name='register_at_shelter'),
    url(r'make-blocks/',PreDRAPComputation.as_view(),name='pre_drap_comp'),
    url(r'compute-block-dict/',BlockDictComputation.as_view(),name='compute_block_dict'),
    url(r'logout/',views.userLogout,name='logout'),
]
