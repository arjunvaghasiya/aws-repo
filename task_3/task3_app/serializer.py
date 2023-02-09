from rest_framework import serializers
from .models import *
import datetime
import re


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=False,
            is_staff=True,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UpdateSerializerProfile(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "current_address",
            "permenent_addresss",
            "age",
            "gender",
            "dte_of_bir",
            "blood_group",
            "phone",
            "user",
        )

    def validate(self, attrs):
        if (
            not re.search(
                "^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$", str(attrs["phone"]))
            or attrs["phone"] == ""
        ):
            raise serializers.ValidationError(
                {"phone": "phone fields should be in 10 digits or in proper format."}
            )
        if attrs["dte_of_bir"] >= datetime.datetime.now().date():
            raise serializers.ValidationError(
                {"Date_of_birth": "Date is invalid,enter valid date"}
            )

        return attrs


class UpdateSerializerCompanyDetails(serializers.ModelSerializer):
    profile = UpdateSerializerProfile(read_only=True)

    class Meta:
        model = CompanyDetails
        fields = (
            "designation",
            "experience",
            "branch_code",
            "project_manager",
            "working_project",
            "salary",
            "is_hr",
            "is_manager",
            "profile",
        )

    def validate(self, attrs):
        company_branches = ["z1", "z2", "z3", "z4", "z5"]
        if (str(attrs["branch_code"]).lower() in company_branches) == False:
            raise serializers.ValidationError(
                {"Branch_code": "ENTER VALID BRANCH CODE"}
            )
        if int(attrs["salary"]) < 0:
            raise serializers.ValidationError(
                {"Salary": "Salary should be graeater than ZERO"}
            )
        return attrs


class UpdateSerializerCompanyDetails_emp_hr(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = (
            "designation",
            "experience",
            "branch_code",
            "project_manager",
            "working_project",
            "salary",
        )

    def validate(self, attrs):
        company_branches = ["z1", "z2", "z3", "z4", "z5"]
        if (str(attrs["branch_code"]).lower() in company_branches) == False:
            raise serializers.ValidationError("ENTER VALID BRANCH CODE")
        if int(attrs["salary"]) < 0:
            raise serializers.ValidationError(
                "Salary should be graeater than ZERO")
        return attrs
