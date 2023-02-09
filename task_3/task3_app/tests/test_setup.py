from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register-list')
  
        self.register_data = {
            'email':'testuser@gmail.com',
            'username':'user@123',
            'first_name':'Ram',
            'last_name':'Vaghasiya',
            'password':'abc123',
            'password2':'abc123'
            
        }

        self.profile_data = {
            'current_address': "Rajkot",
            'permenent_addresss': "Dhoraji",
            'age': "25",
            'gender': "Male",
            'dte_of_bir': "1997-02-02",
            'blood_group': "B Positive",
            'phone': 9623568974,
        }

        self.company_data = {
            'designation':"devloper",
            'experience':"5 years",
            'branch_code':"z5",
            'project_manager':"Virat",
            'working_project':"Amazon sells",
            'salary':7000000,
            'is_hr':False,
            'is_manager':False,
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
