from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pubconnection', views.ConnectionViewpub)

urlpatterns = [

   
    path('', include(router.urls)),
    path("list/connections/pubmyapprovals",views.ConnectionMyApprovalListpub.as_view()),
    # path("pubcontractor_connections/",views.ConnectionViewpub.as_view()),
    path("approvalstatuspub/<pk>/",views.ApprovalStatuspub.as_view()),
    path("pubcontractor_connections/",views.ConnectionContractorViewpub.as_view()),
    path("pubstaff_connections/",views.ConnectionStaffViewpub.as_view()),
    path("pubconnection/approveordeclinete/<pk>/",views.ApproveOrDeclineConnectionTE.as_view()),
    path("pubconnection/approveordeclinepre/<pk>/",views.ApproveOrDeclineConnectionPRE.as_view()),
    path("pubconnection/approveordeclinetest/<pk>/",views.ApproveOrDeclineConnectionTEST.as_view()),
    path("pubconnection/approveordeclinecom/<pk>/",views.ApproveOrDeclineConnectionCOM.as_view()), 
    path("pubconnection/approveordecline/<pk>/",views.ApproveOrDeclineConnectionpub.as_view()),
    path("pubconnection/precommision/list/",views.ContractorConnectionPrecommisionpub.as_view()),
    path("pubconnection/commision/list/",views.ContractorConnectioncommisionpub.as_view()), 
]