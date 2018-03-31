from django.conf.urls import url, include
from django.contrib import admin
from app.views import *
from app import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from app.decorators import *
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
# TODO: Add proper urls
router.register(r'api/civilianUrl', CivilianViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(router.urls, namespace="app")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='app')),

    url(r'google-places/$',GooglePlacesApi.as_view(),name='google-places'),

    #url(r'^register-family/', Civilian().registerFamily),
    url(r'civilian-register/',CivilianRegistrationFormView.as_view(),name='civilian_register'),
    url(r'system-user-register/(?P<role>[a-z]+)/',SystemUserRegistrationFormView.as_view(),name='system_user_register'),
    url(r'login/',LoginFormView.as_view(),name='login'),

	url(r'^admin-home/$', user_is_admin(login_required(AdminHome.as_view())), name='admin-home'),
    url(r'^admin-supplier/$', user_is_admin(login_required(AdminSuppliers.as_view())), name='supplier-details'),
    url(r'^admin-officials/$', user_is_admin(login_required(AdminOfficals.as_view())), name='official-details'),
    url(r'^admin-civilians/$', user_is_admin(login_required(AdminCivilians.as_view())), name='civilian-home'),
    url(r'^admin-shelter/(?P<pk>\d+)/$', user_is_admin(login_required(AdminShelter.as_view())), name='shelter-details-admin'),
    url(r'^shelter-register/$', user_is_admin(login_required(ShelterRegistrationFormView.as_view())), name='shelter-register'),

    url(r'^official-civilians/(?P<pk>\d+)/$', user_is_operator(login_required(OfficialCivilians.as_view())), name='civilian-shelter'),
    url(r'^official-home/(?P<pk>\d+)/$', user_is_operator(login_required(OfficialShelter.as_view())), name='shelter-details-official'),
    url(r'^official-add-civilian/(?P<pk>\d+)/$', user_is_operator(login_required(RegisterAtShelterFormView.as_view())), name='civilian-register-shelter'),
    url(r'allocate-at-shelter/(?P<pk>\d+)/(?P<type>[a-z]+)/',user_is_operator(login_required(AllocationAtShelterFormView.as_view())),name='allocate_at_shelter'),
    url(r'execute-drap/',ExecuteDRAP.as_view(),name='execute_drap'),

    url(r'make-blocks/',PreDRAPComputation.as_view(),name='pre_drap_comp'),
    url(r'compute-block-dict/',BlockDictComputation.as_view(),name='compute_block_dict'),

    url(r'message-receiver/',csrf_exempt(MessageHandler.as_view()),name='message_handler'),

    url(r'get-shelters/',csrf_exempt(GetShelters.as_view()),name='get_shelters'),
    url(r'add-adhoc/',csrf_exempt(AddAdHoc.as_view()),name='add_adhoc'),
    url(r'get-civilian-data/',csrf_exempt(GetCivilianData.as_view()),name='get_civilian_data'),
    url(r'is-disasterous/',csrf_exempt(IsDisasterous.as_view()),name='is_disasterous'),

    url(r'supplier-home/',SupplierFormView.as_view(),name='supply_home'),

    url(r'logout/',login_required(UserLogout.as_view()),name='logout'),
    url(r'fcm_insert/',csrf_exempt(test.as_view())),
]
