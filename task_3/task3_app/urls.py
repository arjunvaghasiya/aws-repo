from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task3_app import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView

router = DefaultRouter()
router.register("register", views.Register_ViewAPI, basename="register")
router.register(
    "adminprofile", views.Admin_Update_Profile_View_API, basename="adminprofile"
)
router.register(
    "admincompanyprofile",
    views.Admin_Update_CompanyDetails_ViewAPI,
    basename="admincompanyprofile",
)
router.register(
    "hrcompanyprofile",
    views.HR_Update_CompanyDetails_ViewAPI,
    basename="hrcompanyprofile",
)
router.register("empprofile", views.EmployeeUpdateProfileViewAPI,
                basename="empprofile")
router.register(
    "empcompanyprofile",
    views.EmployeeUpdateCompanyDetailsViewAPI,
    basename="empcompanyprofile",
)
router.register("employees", views.All_One_Del, basename="employees")

urlpatterns = [
    path("", include(router.urls)),
    path("verify/<token>/<pk>/", views.verify, name="verify"),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
