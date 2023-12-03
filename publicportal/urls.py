from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pubconnection', views.ConnectionViewpub)

urlpatterns = [

   
    path('', include(router.urls)),
    path("list/connections/pubmyapprovals",views.ConnectionMyApprovalListpub.as_view()),
    # path("pubcontractor_connections/",views.ConnectionViewpub.as_view()),
    path("pubconnection/approveordecline/<pk>/",views.ApproveOrDeclineConnectionpub.as_view()),
    path("pubconnection/precommision/list/",views.ContractorConnectionPrecommisionpub.as_view())  
]
