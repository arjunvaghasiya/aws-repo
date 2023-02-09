from .test_setup import TestSetUp
from ..models import *
from rest_framework import status
import datetime


def crt_user_fun(self, is_staff_, is_active_, is_super_user, is_hr_, is_manager_):
    self.client.post(self.register_url, self.register_data, format="json")
    user = User.objects.get(username=self.register_data["username"])
    user.is_active = is_staff_
    user.is_staff = is_active_
    user.is_superuser = is_super_user
    user.save()
    company = CompanyDetails.objects.get(id=user.id)
    company.is_hr = is_hr_
    company.is_manager = is_manager_
    company.save()
    return {
        "username": self.register_data["username"],
        "password": self.register_data["password"],
        "u_id": user.id,
    }


def bearer_auth_for_user(self, a, b):
    res_token = self.client.post(
        path="/api/token/", data={"username": a, "password": b}
    )
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res_token.data['access']}")


def updt_dict(email, username, first_name, last_name, password, password2):
    user_data1 = {
        "email": email,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "password2": password2,
    }
    return user_data1


def crt_user_2(email, username, first_name, last_name, password):
    user = User.objects.create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=False,
        is_staff=True,
    )
    user.set_password(password)
    user.save()
    u2_id = user.id
    return u2_id


def profile_data_user(
    current_address, permenent_addresss, age, gender, dte_of_bir, blood_group, phone
):
    profile_data_user_ = {
        "current_address": current_address,
        "permenent_addresss": permenent_addresss,
        "age": age,
        "gender": gender,
        "dte_of_bir": dte_of_bir,
        "blood_group": blood_group,
        "phone": phone,
    }
    return profile_data_user_


def company_data_user(
    designation, experience, branch_code, project_manager, working_project, salary
):
    company_data_user_ = {
        "designation": designation,
        "experience": experience,
        "branch_code": branch_code,
        "project_manager": project_manager,
        "working_project": working_project,
        "salary": salary,
    }
    return company_data_user_


class TestViews(TestSetUp):
    def test_user_cannot_register_with_blank_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_register_with_data(self):
        res = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(res.data["Email"], self.register_data["email"])
        self.assertEqual(res.data["UserName"], self.register_data["username"])
        self.assertEqual(res.status_code, 201)

    def test_user_register_with_unmatch_passwordfield(self):
        reg_data = updt_dict(
            "test@gmail.com", "test123", "ram", "raj", "password123", "password321"
        )
        res = self.client.post(self.register_url, data=reg_data, format="json")
        self.assertEqual(res.status_code, 400)

    ##################################################################################
    # FETCH LIST OF ALL EMPLOYEE

    def test_Admin_get_list_user_req(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/employees/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_Admin_get_list_user_req_pagenation(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/employees/?is_hr=true"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    ##################################################################################
    # FETCH ONE EMPLOYEE WITH VALID AND INVALID DATA

    def test_Admin_get_one_user(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/employees/{user2_id}/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_Admin_get_one_invalid_user(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/employees/3333/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    ##################################################################################
    # TEST DELETE API WITH VALID AND INVALID DATA

    def test_Admin_delete_one_user(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/employees/{user2_id}/"
        response3 = self.client.delete(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_Admin_delete_user_Invalid_id(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/employees/3/"
        response3 = self.client.delete(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    ###################################################################################
    # EMPLOYEE GET REQUEST FOR RETRIVE EMPLOYEE DETAIL

    def test_employee_profile_get_req(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        api_url = f"/empprofile/{u_id}/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_employee_company_get_req(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        api_url = f"/empcompanyprofile/{u_id}/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    ####################################################################################
    # EMPLOYEE PUT REQUEST FOR UPDATE EMPLOYEE DETAIL

    def test_employee_updt_profile_put_req(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        api_url = f"/empprofile/{u_id}/"
        response3 = self.client.put(api_url, data=self.profile_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_employee_updt_company_put_req(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        api_url = f"/empcompanyprofile/{u_id}/"
        response3 = self.client.put(api_url, data=self.company_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    ###################################################################################
    # TRY TO EMPLOYEE GET REQUEST FOR RETRIVE EMPLOYEE DETAIL USING INVALID ID

    def test_employee_updt_profile_get_req_with_invalid_id(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/empprofile/32/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_updt_company_get_req_with_invalid_id(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/empcompanyprofile/32/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    ###################################################################################
    # TRY TO ACCESS OTHER REGISTERD EMPLOYEE BY ANOTHER EMPLOYEE

    def test_employee_updt_profile_get_req_with_registered_user_id(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/empprofile/{user2_id}/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_updt_company_get_req_with_registered_user_id(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/empcompanyprofile/{user2_id}/"
        response3 = self.client.get(api_url, format="json")
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)

    ###################################################################################
    # TRY TO EMPLOYEE PUT REQUEST FOR UPDATE EMPLOYEE DETAIL USING INVALID ID

    def test_employee_updt_profile_put_req_with_invalid_id(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/empprofile/32/"
        response3 = self.client.put(api_url, data=self.profile_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_updt_company_put_req_with_invalid_id(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        api_url = f"/empcompanyprofile/32/"
        response3 = self.client.put(api_url, data=self.company_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    ###################################################################################
    # BY EMPLOYEE CHECK FOR INVALID PHONE, DATE_OF_BIRTH, BRANCH_CODE, SALARY

    # INVALID PHONE
    def test_employee_updt_profile_put_req_INVALID_PHONE(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        x = f"/empprofile/{u_id}/"
        serializer_data = profile_data_user(
            "Rajkot", "Junagadh", 32, "Male", "1998-03-03", "B positive", 9855555555555
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    # INVALID DATE_OF_BIRTH
    def test_employee_updt_profile_put_req_INVALID_DATE(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        x = f"/empprofile/{u_id}/"
        serializer_data = profile_data_user(
            "Rajkot",
            "Junagadh",
            32,
            "Male",
            datetime.datetime.now().date(),
            "B positive",
            9653264785,
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    # INVALID BRANCH_CODE
    def test_employee_updt_company_put_req_INVALID_BRANCH_CODE(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        x = f"/empcompanyprofile/{u_id}/"
        serializer_data = company_data_user(
            "Software Dev", "10 years", "z9", "Rahul", "TCS", 700000
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    # INVALID SALARY
    def test_employee_updt_company_put_req_INVALID_SALARY(self):
        user_crt = crt_user_fun(self, True, True, False, False, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        u_id = user_crt["u_id"]
        x = f"/empcompanyprofile/{u_id}/"
        serializer_data = company_data_user(
            "Software Dev", "10 years", "z2", "Rahul", "TCS", -700000
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    ###################################################################################
    # ADMIN UPDATE EMPLOYEE USING GET REQ

    def test_Admin_updt_profile_put_req(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        x = f"/adminprofile/{user2_id}/"
        serializer_data = profile_data_user(
            "Rajkot", "Junagadh", 32, "Male", "1998-03-03", "B positive", 9875635698
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_Admin_updt_company_put_req(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        x = f"/admincompanyprofile/{user2_id}/"
        serializer_data = company_data_user(
            "Software Dev", "10 years", "z2", "Rahul", "TCS", 700000
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    ###################################################################################
    # BY ADMIN UPDATE EMPLOYEE INVALID BRANCH_CODE, SALARY

    # INVALID BRANCH_CODE
    def test_Admin_updt_company_put_req_INVALID_BRANCH_CODE(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        x = f"/admincompanyprofile/{user2_id}/"
        serializer_data = company_data_user(
            "Software Dev", "10 years", "z9", "Rahul", "TCS", 700000
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    # INVALID SALARY
    def test_Admin_updt_company_put_req_INVALID_SALARY(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, True, True, True)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        x = f"/admincompanyprofile/{user2_id}/"
        serializer_data = company_data_user(
            "Software Dev", "10 years", "z2", "Rahul", "TCS", -700000
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    ###################################################################################
    # HR UPDATE EMPLOYEE USING GET REQ

    def test_Hr_updt_profile_put_req(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, False, True, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        x = f"/adminprofile/{user2_id}/"
        serializer_data = profile_data_user(
            "Rajkot", "Junagadh", 32, "Male", "1998-03-03", "B positive", 9875635698
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_Hr_updt_company_put_req(self):
        user2_id = crt_user_2("test@gmail.com", "test123", "ram", "raj", "password123")
        user_crt = crt_user_fun(self, True, True, False, True, False)
        bearer_auth_for_user(self, user_crt["username"], user_crt["password"])
        x = f"/hrcompanyprofile/{user2_id}/"
        serializer_data = company_data_user(
            "Software Dev", "10 years", "z2", "Rahul", "TCS", 700000
        )
        response3 = self.client.put(x, data=serializer_data, format="json")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
