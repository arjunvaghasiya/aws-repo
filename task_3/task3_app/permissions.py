from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
)
from .models import *


class IsAdminUser_ForAdmin(BasePermission):
    def has_permission(self, request, view):
        # import pdb;pdb.set_trace()
        return bool(
            request.user and request.user.is_staff and request.user.is_superuser
        )


class IsHRUser_ForHr(BasePermission):
    def has_permission(self, request, view):
        # import pdb;pdb.set_trace()
        user_pro = CompanyDetails.objects.get(
            id=(Profile.objects.get(user=request.user)).id
        )
        if user_pro.is_hr == True:
            user_permission = True
        else:
            user_permission = False

        return bool(request.user and request.user.is_staff and user_permission)


class IsManagerUser_ForManager(BasePermission):
    def has_permission(self, request, view):
        # import pdb;pdb.set_trace()
        user_pro = CompanyDetails.objects.get(
            id=(Profile.objects.get(user=request.user)).id
        )
        if user_pro.is_manager == True:
            user_permission = True
        else:
            user_permission = False

        return bool(request.user and request.user.is_staff and user_permission)
