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

    url(r'register-at-shelter/',user_is_operator(login_required(RegisterAtShelterFormView.as_view())),name='register_at_shelter'),
    url(r'allocate-at-shelter/(?P<type>[a-z]+)/',user_is_operator(login_required(AllocationAtShelterFormView.as_view())),name='allocate_at_shelter'),
    url(r'make-blocks/',PreDRAPComputation.as_view(),name='pre_drap_comp'),
    url(r'compute-block-dict/',BlockDictComputation.as_view(),name='compute_block_dict'),
]
