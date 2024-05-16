
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path("admin/", admin.site.urls),
# ]
from django.urls import include, path
from rest_framework import routers
from portal import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


router = routers.DefaultRouter()
router.register('connections', views.ConnectionView)
router.register('contractors', views.contractor_regview)
# router.register('technical',views.technicalview)
router.register('list_connections',views.contractStaffListOnlyview)

router.register('rh', views.regionview)
router.register('bh', views.businesshubview)
router.register('bhlist', views.businesshublistview)
router.register('rhlist', views.regionlistview)
# router.register('contractor_connections', views.ConnectionContractorView)


#router.register('account', include('allauth.urls'))



urlpatterns = [
    path('public/', include('publicportal.urls')),
    path('', include(router.urls)),
    # path('accounts/', include('allauth.urls')),
    path("admin/", admin.site.urls),
    path("login/",views.LoginView.as_view()),
    path("signup/",views.RegisterView.as_view()),
    path("logout/",views.LogoutView.as_view()),
    path("list/user/staff",views.UserList.as_view()),
    path("list/user/contractors",views.ContractorList.as_view()),
    path("list/user/unsubmitcontractors",views.ContractorListunsubmit.as_view()),
    path("list/myapprovals",views.ContractorMyApprovalList.as_view()),
    path("list/connections/myapprovals",views.ConnectionMyApprovalList.as_view()),
    # path("approveordecline/<pk>/",views.ApproveOrDeclineContractor.as_view()),
    path("approveordecline/<pk>/",views.ApproveOrDeclineContractor.as_view()),
    path("approvalstatus/<pk>/",views.ApprovalStatus.as_view()),
    path("contractor_connections/",views.ConnectionContractorView.as_view()),
    path("staff_connections/",views.ConnectionStaffView.as_view()),
    path("connection/approveordecline/<pk>/",views.ApproveOrDeclineConnection.as_view()),
    path("connection/precommision/list/",views.ContractorConnectionPrecommision.as_view()),
    path("connection/commision/list/",views.ContractorCommision.as_view()),
    
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    path("updatecontractorreg/<pk>/",views.contractor_regupdatesubmitview.as_view()),
    
       
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="NEW CONNECTION PORTAL"
admin.site.site_title="NCP"
admin.site.index_title="WELCOME TO NCP"