from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from task3_app.serializer import *
from django.http import JsonResponse
from .permissions import *
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .pagination import CustomPageNumberPagination
import django_filters.rest_framework

# Create your views here.


def send_mail(user, token, pk):
    # import pdb;pdb.set_trace()
    email = EmailMessage(
        subject="verify email",
        body=f"Hi verify your account by click this LINK \n \n  http://127.0.0.1:8000/verify/{token}/{pk}",
        to=[user],
    )
    email.send()


def verify(request, token, pk):
    # import pdb;pdb.set_trace()
    user = User.objects.get(username=pk)
    user.is_active = True
    user.save()
    return HttpResponse("<h1>you have registerd succesfully </h1>")


class All_One_Del(viewsets.ViewSet):
    queryset = CompanyDetails.objects.all()
    # pagination_class = CustomPageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["is_hr", "is_manager"]

    permission_classes_by_action = {
        "list": [IsAdminUser_ForAdmin | IsHRUser_ForHr | IsManagerUser_ForManager],
        "retrive": [IsAdminUser_ForAdmin | IsHRUser_ForHr | IsManagerUser_ForManager],
        "destroy": [IsAdminUser_ForAdmin | IsHRUser_ForHr],
    }

    def list(self, request):
        user = CompanyDetails.objects.all()
        queryset = self.filter_queryset(user)
        paginator = CustomPageNumberPagination()
        objects = paginator.paginate_queryset(queryset, request)
        serializer = UpdateSerializerCompanyDetails(objects, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def retrieve(self, request, pk=None):
        try:
            user = CompanyDetails.objects.get(id=pk)
        except CompanyDetails.DoesNotExist:
            return Response(
                {"msg": "There is no User With this ID"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UpdateSerializerCompanyDetails(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            User.objects.get(id=pk).delete()
        except User.DoesNotExist:
            return Response(
                {"msg": "There is no User With this ID"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({"msg": "User deleted"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class Register_ViewAPI(viewsets.ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # import pdb;pdb.set_trace()
        pk = User.objects.get(email=serializer.data["email"])
        refresh = RefreshToken.for_user(pk)
        send_mail(serializer.data["email"], refresh.access_token, pk)
        context = {}
        context = dict(request.data)
        response_data = {
            "UserName": context["username"],
            "Email": context["email"],
            "Token Access": str(refresh.access_token),
            "Token Refresh": str(refresh),
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)


class Admin_Update_Profile_View_API(viewsets.ViewSet):
    serializer_class = UpdateSerializerProfile
    permission_classes = [IsAdminUser_ForAdmin | IsHRUser_ForHr]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def update(self, request, pk=None):
        user = Profile.objects.get(id=pk)
        serializer = UpdateSerializerProfile(user, data=request.data)
        # import pdb;pdb.set_trace()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class Admin_Update_CompanyDetails_ViewAPI(viewsets.ViewSet):
    serializer_class = UpdateSerializerCompanyDetails
    permission_classes = [
        IsAdminUser_ForAdmin,
    ]
    # import pdb;pdb.set_trace()
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def update(self, request, pk=None):
        # import pdb;pdb.set_trace()
        profile = CompanyDetails.objects.get(id=pk)
        serializer = UpdateSerializerCompanyDetails(profile, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class HR_Update_CompanyDetails_ViewAPI(viewsets.ViewSet):
    serializer_class = UpdateSerializerCompanyDetails_emp_hr
    permission_classes = [IsAuthenticated, IsHRUser_ForHr]
    # import pdb;pdb.set_trace()
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def update(self, request, pk=None):
        # import pdb;pdb.set_trace()
        profile = CompanyDetails.objects.get(id=pk)
        serializer = UpdateSerializerCompanyDetails_emp_hr(
            profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class EmployeeUpdateProfileViewAPI(viewsets.ViewSet):
    serializer_class = UpdateSerializerProfile
    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def retrieve(self, request, pk=None):
        # import pdb;pdb.set_trace()
        try:
            profile = Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return Response(
                {"msg": "There is no User With this ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdateSerializerProfile(profile)
        if int(pk) == request.user.id:
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "msg": "Invalid ID ..!! your id is not matched with id that you have mentioned in urls"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def update(self, request, pk=None):
        try:
            user = Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return Response(
                {"msg": "There is no User With this ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdateSerializerProfile(user, data=request.data)
        # import pdb;pdb.set_trace()
        if serializer.is_valid(raise_exception=True) and request.user.id == int(pk):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class EmployeeUpdateCompanyDetailsViewAPI(viewsets.ViewSet):
    serializer_class = UpdateSerializerCompanyDetails_emp_hr
    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def retrieve(self, request, pk=None):
        # import pdb;pdb.set_trace()
        try:
            company = CompanyDetails.objects.get(id=pk)
        except CompanyDetails.DoesNotExist:
            return Response(
                {"msg": "There is no User With this ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdateSerializerCompanyDetails_emp_hr(company)
        if int(pk) == request.user.id:
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "msg": "Invalid ID ..!! your id is not matched with id that you have mentioned in urls"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def update(self, request, pk=None):
        try:
            user = CompanyDetails.objects.get(id=pk)
        except CompanyDetails.DoesNotExist:
            return Response(
                {"msg": "There is no User With this ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdateSerializerCompanyDetails_emp_hr(
            user, data=request.data)
        # import pdb;pdb.set_trace()
        if serializer.is_valid(raise_exception=True) and request.user.id == int(pk):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
