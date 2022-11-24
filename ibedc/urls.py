
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
router.register('supplier', views.contractview)
router.register('contractors', views.contractor_regview)
router.register('technical',views.technicalview)
router.register('list_contractors',views.contractListOnlyview)
router.register('rh', views.regionview)
router.register('bh', views.businesshubview)
router.register('bhlist', views.businesshublistview)

#router.register('account', include('allauth.urls'))



urlpatterns = [
    path('', include(router.urls)),
    # path('accounts/', include('allauth.urls')),
    path("admin/", admin.site.urls),
    path("login/",views.LoginView.as_view()),
    path("signup/",views.RegisterView.as_view()),
    path("logout/",views.LogoutView.as_view()),
    path("list/user/staff",views.UserList.as_view()),
    path("list/user/contractors",views.UserList.as_view()),
       
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="NEW CONNECTION PORTAL"
admin.site.site_title="NCP"
admin.site.index_title="WELCOME TO NCP"